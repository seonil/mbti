# -*- coding: utf-8 -*-
import json
from itertools import cycle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MBTI_SEQUENCE = [
    "ENFP", "ENFJ", "ENTP", "ENTJ",
    "INFJ", "INFP", "INTP", "INTJ",
    "ESFP", "ESFJ", "ESTP", "ESTJ",
    "ISFP", "ISFJ", "ISTP", "ISTJ"
]

WRONG_PHRASES = [
    "야! 그냥 질러봅시다. 나중에 생각하죠!",
    "이건 대충 넘어가도 되죠?",
    "일단 결론부터 말할게요. 내일 다시 얘기해요.",
    "그냥 네가 알아서 해.",
    "회의는 여기서 끝! 세부 계획은 생략할게요.",
    "그냥 마음 가는 대로 해보죠?",
    "굳이 보고할 필요 없겠죠?",
    "일단 즐기고 나중에 수습하죠!",
    "내가 알아서 정리했다 치고 넘어가죠.",
    "다음 주에 기억나면 말해줄게요.",
    "일단 결과는 운에 맡겨요.",
    "조금 대충해도 괜찮겠죠?",
    "기록은 필요 없겠지요?",
    "어차피 다들 알겠죠?",
    "회의 끝! 근데 계획은 추후 공유할게요.",
    "일단 감으로 가봅시다.",
    "대충 해도 다 알아서 굴러갈 거예요.",
    "일단 저질러놓고 보죠!",
    "바쁘니까 이건 생략해도 되죠?",
    "오늘은 대충 마무리합시다."
]

def load_data():
    data_path = BASE_DIR / "mbti_data.json"
    return json.loads(data_path.read_text(encoding="utf-8"))

def build_quiz(data):
    closing_cycle = cycle(WRONG_PHRASES)
    for key, info in data.items():
        moves = info["battle"]["moves"]
        power = info["powerItems"]
        quick_phrases = info["quickPhrases"]
        wrong1 = next(closing_cycle)
        wrong2 = next(closing_cycle)

        cards = [
            {
                "round": "ROUND 1",
                "title": "전략 오프닝",
                "prompt": f"{info['nickname']}과(와)의 첫 라운드! 어떤 액션으로 시작할까?",
                "hint": info["battle"]["intro"],
                "options": [
                    {"label": moves[0]["name"], "isCorrect": True, "feedback": moves[0]["detail"]},
                    {"label": moves[1]["name"], "isCorrect": False, "feedback": moves[1]["detail"] + " — 아직은 타이밍이 아니에요."},
                    {"label": moves[2]["name"], "isCorrect": False, "feedback": moves[2]["detail"] + " — 마무리 단계용 카드입니다."}
                ],
                "success": "완벽한 스타트!",
                "failure": "시작부터 삐끗했어요. 타이밍을 다시 조율해요."
            },
            {
                "round": "ROUND 2",
                "title": "파워 아이템 세팅",
                "prompt": f"{info['nickname']}에게 가장 필요한 지원 장비는?",
                "hint": f"약점을 메워줄 장비를 선택하세요. {power['weakSpot']}을(를) 보완해야 합니다.",
                "options": [
                    {"label": power["support"], "isCorrect": True, "feedback": f"{power['support']}이(가) 있어야 {info['nickname']}의 강점이 폭발해요."},
                    {"label": power["ally"], "isCorrect": False, "feedback": f"{power['ally']}은(는) 동료예요. 장비가 아닙니다."},
                    {"label": power["weakSpot"], "isCorrect": False, "feedback": f"{power['weakSpot']}은(는) 관리해야 할 약점이에요."}
                ],
                "success": "장비 세팅 완료!",
                "failure": "장비 선택을 다시 생각해봐요."
            },
            {
                "round": "ROUND 3",
                "title": "클로징 멘트",
                "prompt": f"{info['nickname']}에게 마지막으로 건넬 멘트는?",
                "hint": "감정선과 전략을 동시에 잡을 수 있는 말을 고르세요.",
                "options": [
                    {"label": quick_phrases[0], "isCorrect": True, "feedback": "이 멘트가 바로 신뢰를 높이는 한마디예요."},
                    {"label": wrong1, "isCorrect": False, "feedback": "이 멘트는 분위기를 깨고 신뢰를 떨어뜨립니다."},
                    {"label": wrong2, "isCorrect": False, "feedback": "상대에게 부담만 주는 멘트입니다."}
                ],
                "success": "완벽한 마무리!",
                "failure": f"{info['nickname']}의 감정선과 맞지 않는 마무리였어요."
            }
        ]

        info["quiz"] = {
            "cards": cards,
            "summary": {
                "title": f"{key} 생존 시뮬레이션 결과",
                "winMessage": info["battle"]["finale"],
                "loseMessage": f"{info['nickname']}과(와)의 동맹을 위해 전략을 다시 세워보세요."
            }
        }

def render_html(data):
    template_path = BASE_DIR / "template.html"
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__MBTI_DATA__", json.dumps(data, ensure_ascii=False, indent=2))
    html = html.replace("__MBTI_SEQUENCE__", json.dumps(MBTI_SEQUENCE, ensure_ascii=False))
    (BASE_DIR / "index.html").write_text(html, encoding="utf-8")
    print("index.html generated")

def main():
    data = load_data()
    build_quiz(data)
    render_html(data)

if __name__ == "__main__":
    main()
