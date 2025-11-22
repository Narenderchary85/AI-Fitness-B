from flask import Blueprint, request, jsonify
from utils import build_plan_prompt
from ai import call_perplexity_api, parse_json_from_text, generate_tts, generate_image_bfl
from models import save_plan, get_plan_by_id, get_user_by_id
import traceback
from utils import serialize_mongo
import requests

plans = Blueprint('plans', __name__)


@plans.route('/generate', methods=['POST'])
def generate_plan():
    try:
        payload = request.get_json() or {}

        user_details = payload.get('user_details')
        if not user_details:
            return jsonify({"success": False, "message": "Missing user_details"}), 400

        prompt = build_plan_prompt(user_details)
        raw = call_perplexity_api(prompt)
        parsed = parse_json_from_text(raw)

        if not parsed:
            return jsonify({
                "success": False,
                "message": "Failed to parse LLM output",
                "raw": raw
            }), 500

        plan_doc = {
            "user_details": user_details,
            "plan": parsed,
            "llm_raw": raw
        }

        saved = save_plan(None, plan_doc)

        saved = serialize_mongo(saved)

        return jsonify({"success": True, "plan": saved}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500



@plans.route('/<plan_id>', methods=['GET'])
def get_plan(plan_id):
    try:
        plan = get_plan_by_id(plan_id)
        if not plan:
            return jsonify({"success": False, "message": "Not found"}), 404

        plan = serialize_mongo(plan)
        return jsonify({"success": True, "plan": plan})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@plans.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json() or {}
        text = data.get('text')
        if not text:
            return jsonify({"success": False, "message": "Missing text"}), 400

        audio_bytes = generate_tts(text)

        import base64
        b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return jsonify({"success": True, "audio_base64": b64})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"success": False, "message": str(e)}), 500



@plans.route('/image', methods=['POST'])
def image_gen():
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({"success": False, "message": "Missing prompt"}), 400

        result = generate_image_bfl(prompt)
        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

