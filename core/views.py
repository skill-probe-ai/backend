
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume,Skill,UserSkill,InterviewSession,Question,Answer
from .serializers import ResumeSerializer
from django.contrib.auth.models import User
from .llm import extract_skills,generate_question,evaluate_answer
import json
from .utils import safe_parse_json  # if you moved it

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class PlainTextParser:
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return {"answer": stream.read().decode('utf-8')}


class ResumeView(APIView):

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            resume = serializer.save(user=request.user)

            # 🔥 Extract skills using LLM
            skills_json = extract_skills(resume.content)

            print("RAW LLM RESPONSE:", skills_json)

            try:
                skills_list = json.loads(skills_json)
                print("SKILLS LIST:", skills_list)
            except:
                skills_list = []

            for skill_name in skills_list:
                print("Saving skill:", skill_name)

                skill, _ = Skill.objects.get_or_create(name=skill_name)

                UserSkill.objects.get_or_create(
                    user=request.user,
                    skill=skill
                )

            return Response({
                "resume": serializer.data,
                "skills": skills_list
            })

        return Response(serializer.errors)
    

class StartInterviewView(APIView):

    def post(self, request):
        skill_name = request.data.get("skill").strip()

        skill = Skill.objects.filter(name__iexact=skill_name).first()
        if not skill:
            return Response({"error": "Skill not found"}, status=400)

        user = User.objects.first()

        total_questions = request.data.get("total_questions", 5)

        session = InterviewSession.objects.create(
            user=user,
            skill=skill,
            total_questions=total_questions
        )

        difficulty = "easy"

        question_text = generate_question(skill.name, difficulty)

        question = Question.objects.create(
            session=session,
            text=question_text,
            difficulty=difficulty
        )

        return Response({
            "question": question.text,
            "question_id": question.id,
            "session_id": session.id,
            "difficulty": difficulty
        })



        
class SubmitAnswerView(APIView):

    parser_classes = [JSONParser, FormParser, MultiPartParser, PlainTextParser]

    def post(self, request):
        session_id = request.data.get("session_id") or request.query_params.get("session_id")
        question_id = request.data.get("question_id") or request.query_params.get("question_id")

        answer_text = request.data.get("answer")
        if not answer_text:
            answer_text = request.body.decode("utf-8")

        session = InterviewSession.objects.get(id=session_id)
        question = Question.objects.get(id=question_id)

        # evaluate
        raw_result = evaluate_answer(
            session.skill.name,
            question.text,
            answer_text,
            question.difficulty
        )
        result = safe_parse_json(raw_result)

        score = result.get("score")
        if isinstance(score, str):
            try:
                score = float(score)
            except:
                score = None

        Answer.objects.create(
            question=question,
            text=answer_text,
            score=score,
            feedback=result.get("feedback"),
            improvement=result.get("improvement")
        )

        # update session progress
        session.current_question_index += 1

        # check if completed
        if session.current_question_index >= session.total_questions:
            session.is_completed = True
            session.save()

            return self.get_final_result(session,result)

        # determine next difficulty
        index = session.current_question_index

        if index == 0:
            difficulty = "easy"
        elif index == 1:
            difficulty = "easy"
        elif index in [2, 3]:
            difficulty = "medium"
        else:
            difficulty = "hard"

        # generate next question
        next_q_text = generate_question(session.skill.name, difficulty)

        next_question = Question.objects.create(
            session=session,
            text=next_q_text,
            difficulty=difficulty
        )

        session.save()

        return Response({
            "score": score,
            "feedback": result.get("feedback"),
            "improvement": result.get("improvement"),
            "next_question": next_question.text,
            "question_id": next_question.id,
            "difficulty": difficulty,
            "progress": f"{session.current_question_index}/{session.total_questions}"
        })
    
    
    

    def get_final_result(self, session, result):
        answers = Answer.objects.filter(question__session=session)

        scores = [a.score for a in answers if a.score is not None]

        avg_score = sum(scores) / len(scores) if scores else 0


        if avg_score >= 8:
            level = "Advanced"
        elif avg_score >= 6:
            level = "Intermediate"
        else:
            level = "Beginner"

        #  verification logic
        is_verified = avg_score >= 7

        # update user skill
        user_skill, _ = UserSkill.objects.get_or_create(
            user=session.user,
            skill=session.skill
        )

        user_skill.verification_score = avg_score
        user_skill.is_verified = is_verified
        user_skill.save()

        return Response({
            "message": "Interview completed",
            "average_score": round(avg_score, 2),
            "level": level,
            "verified": is_verified,
            "skill": session.skill.name,
            "feedback": result.get("feedback"),
            "improvement": result.get("improvement"),
        })