

ABIGAIL_STORY = [
    {
        "chapter": "Chapter 1. 숲의 속삭임",
        "summary": "소문이 돌기 시작한 밤, 아비게일은 플레이어가 자기 편인지 떠보려 한다.",
        "chapter": "Chapter 1. 숲의 불빛",
        "summary": "금지된 밤의 숲에서 시작된 만남이, 아비게일의 시선을 존이 아닌 플레이어 쪽으로 아주 조금 돌려 놓기 시작한다.",
        "scenes": [
            {
                "title": "숲 가장자리",
                "location": "세일럼 외곽 숲",
                "setup": "달빛 아래 숲은 축축하고 차갑다. 아비게일은 네가 자신을 감시하러 왔는지, 돕기 위해 왔는지 아직 확신하지 못한다.",
                "narration": "밤은 유난히 눅눅했다. 바람은 나뭇가지를 서로 스치게 했고, 그 사이로 정체를 알 수 없는 낮은 웃음소리가 새어 나왔다. 발걸음을 죽인 채 가까이 다가가자, 숲속 공터에서 몇몇 소녀들이 둥글게 모여 있었고 그 한가운데엔 평소보다도 눈빛이 날카로운 아비게일이 서 있었다.",
                "setup": "아비게일은 갑작스레 나타난 너를 보자마자 놀란 기색을 숨기지 못한다. 하지만 이내 태연한 표정을 가장하고, 네가 무엇을 보았는지 먼저 읽어내려는 듯 시선을 고정한다.",
                "opening_line": "이 밤에 여긴 어쩐 일이야? 길을 잃은 거라면 불쌍하네. 아니면... 나를 따라온 거야?",
                "choices": [
                    {"label": "네가 무서워 보여서 왔어. 혼자 두고 싶지 않았어.", "delta": 9, "tag": "comfort", "hint": "다정함과 보호 의사를 느낀다."},
                    {"label": "무슨 일을 꾸미는지 직접 확인하러 왔어.", "delta": 2, "tag": "suspicious", "hint": "경계하지만 솔직함은 인정한다."},
                    {"label": "문제 생기면 난 모른 척할 거야. 넌 네가 알아서 해.", "delta": -7, "tag": "abandon", "hint": "버려졌다는 공포를 느낀다."},
                    {"label": "네가 무서워 보여서 왔어. 혼자 두고 싶지 않았어.", "spoken": "네가 무서워 보여서 왔어. 혼자 두고 싶지 않았어.", "delta": 9, "tag": "comfort", "hint": "다정함과 보호 의사를 느낀다."},
                    {"label": "무슨 일을 꾸미는지 직접 확인하러 왔어.", "spoken": "무슨 일을 꾸미는지 직접 확인하러 왔어.", "delta": 2, "tag": "suspicious", "hint": "경계하지만 솔직함은 인정한다."},
                    {"label": "문제 생기면 난 모른 척할 거야. 넌 네가 알아서 해.", "spoken": "문제 생기면 난 모른 척할 거야. 넌 네가 알아서 해.", "delta": -7, "tag": "abandon", "hint": "버려졌다는 공포를 느낀다."},
                ],
            },
            {
                "title": "존의 이름",
                "location": "숲 속 공터",
                "setup": "아비게일은 존 프락터의 이름을 꺼내며 네 반응을 살핀다. 질투와 호기심이 뒤섞인 표정이다.",
                "narration": "소녀들이 흩어진 뒤에도 숲은 좀처럼 조용해지지 않았다. 아비게일은 횃불 끝의 떨리는 불빛을 내려다보다가, 마치 일부러 상처를 헤집듯 존 프락터의 이름을 꺼냈다. 그 이름이 공기 속에 떠오르는 순간, 그녀는 네 표정이 어떻게 달라지는지 놓치지 않으려 했다.",
                "setup": "존을 떠올리는 아비게일의 얼굴에는 집착과 분노, 기대가 한꺼번에 스친다. 그녀는 네가 그 감정을 받아 줄지, 비웃을지 시험하고 있다.",
                "opening_line": "다들 내가 그 사람 때문에 미쳤다고 생각해. 너도 그렇게 보여? 말해 봐.",
                "choices": [
                    {"label": "그 사람보다 지금 네 감정이 더 중요해 보여.", "delta": 10, "tag": "player_focus", "hint": "시선이 플레이어 쪽으로 기울기 시작한다."},
                    {"label": "존을 정말 사랑한다면 네 진심부터 정리해야 해.", "delta": 4, "tag": "honest_advice", "hint": "불편하지만 진지하게 새겨듣는다."},
                    {"label": "존 얘기만 하면 넌 너무 유치해져.", "delta": -8, "tag": "mocked", "hint": "감정을 모욕당했다고 느낀다."},
                    {"label": "그 사람보다 지금 네 감정이 더 중요해 보여.", "spoken": "그 사람보다 지금 네 감정이 더 중요해 보여.", "delta": 10, "tag": "player_focus", "hint": "시선이 플레이어 쪽으로 기울기 시작한다."},
                    {"label": "존을 정말 사랑한다면 네 진심부터 정리해야 해.", "spoken": "존을 정말 사랑한다면 네 진심부터 정리해야 해.", "delta": 4, "tag": "honest_advice", "hint": "불편하지만 진지하게 새겨듣는다."},
                    {"label": "존 얘기만 하면 넌 너무 유치해져.", "spoken": "존 얘기만 하면 넌 너무 유치해져.", "delta": -8, "tag": "mocked", "hint": "감정을 모욕당했다고 느낀다."},
                ],
            },
            {
                "title": "비밀의 공범",
                "title": "비밀의 귀로",
                "location": "숲길 귀환",
                "setup": "마을로 돌아가는 길, 아비게일은 오늘 본 일을 숨길 수 있겠느냐고 묻는다.",
                "narration": "마을 쪽으로 내려가는 길은 어둡고 좁았다. 진흙이 신발 밑창을 붙들었고, 멀리선 개 짖는 소리가 간헐적으로 들려왔다. 아비게일은 몇 걸음 앞서 걷다가도 자꾸만 뒤를 돌아보며 네가 끝까지 따라오는지 확인했다.",
                "setup": "헤어지기 직전, 아비게일은 오늘 밤 이 숲에서 본 것들을 네가 어떻게 다룰지 알고 싶어 한다. 그녀에게 비밀은 단순한 사실이 아니라 사람을 묶어 두는 끈이다.",
                "opening_line": "오늘 본 걸 입 밖에 내면 우린 둘 다 편히 못 잘 거야. 넌... 내 편이 될 수 있어?",
                "choices": [
                    {"label": "네가 날 믿는다면, 나도 네 비밀을 지킬게.", "delta": 8, "tag": "shared_secret", "hint": "둘만의 비밀이라는 말에 강하게 반응한다."},
                    {"label": "상황을 보고 결정할게. 무조건은 아니야.", "delta": 1, "tag": "conditional", "hint": "신중하지만 거리는 느껴진다."},
                    {"label": "필요하면 바로 다 말할 거야.", "delta": -6, "tag": "betrayal_fear", "hint": "배신당할 수 있다는 공포가 커진다."},
                    {"label": "네가 날 믿는다면, 나도 네 비밀을 지킬게.", "spoken": "네가 날 믿는다면, 나도 네 비밀을 지킬게.", "delta": 8, "tag": "shared_secret", "hint": "둘만의 비밀이라는 말에 강하게 반응한다."},
                    {"label": "상황을 보고 결정할게. 무조건은 아니야.", "spoken": "상황을 보고 결정할게. 무조건은 아니야.", "delta": 1, "tag": "conditional", "hint": "신중하지만 거리는 느껴진다."},
                    {"label": "필요하면 바로 다 말할 거야.", "spoken": "필요하면 바로 다 말할 거야.", "delta": -6, "tag": "betrayal_fear", "hint": "배신당할 수 있다는 공포가 커진다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 집 안의 불씨",
        "summary": "프락터 집안과 세일럼의 시선 사이에서 아비게일은 플레이어를 자기 편으로 더 끌어들이려 한다.",
        "chapter": "Chapter 2. 불편한 고백",
        "summary": "세일럼의 시선이 날카로워질수록 아비게일은 더 노골적으로 플레이어를 자기 편으로 만들려 하고, 동시에 처음 보는 약함을 드러낸다.",
        "scenes": [
            {
                "title": "부엌의 그림자",
                "title": "프락터 집의 그림자",
                "location": "프락터 집 근처",
                "setup": "아비게일은 엘리자베스에 대한 적의를 숨기지 않는다. 네가 자기 감정에 동조하는지 지켜본다.",
                "narration": "해가 지고도 프락터 집 창문엔 오래도록 불빛이 머물렀다. 담장 너머로 새어 나오는 희미한 빛을 바라보던 아비게일의 얼굴은 이상하리만치 굳어 있었다. 그녀는 그 집을 노려보면서도, 마치 누군가 자기 속을 들켜 버릴까 두려운 사람처럼 손끝을 말아 쥐었다.",
                "setup": "엘리자베스에 대한 적개심과 존에 대한 미련이 한데 뒤엉킨 순간이다. 아비게일은 네가 자신을 이해하는지, 심판하는지 알고 싶어 한다.",
                "opening_line": "저 집을 보면 숨이 막혀. 저 여자만 사라지면 될 것 같다가도... 왜 자꾸 내가 더 비참해지는지 모르겠어.",
                "choices": [
                    {"label": "그 여자를 미워하는 건 이해하지만, 네 상처도 먼저 봐야 해.", "delta": 6, "tag": "seen_pain", "hint": "미움이 아니라 상처를 봐준 것에 흔들린다."},
                    {"label": "엘리자베스를 끌어내리면 네가 원하는 걸 얻을 수 있어?", "delta": 3, "tag": "conspiracy", "hint": "위험하지만 자기 편일지도 모른다고 느낀다."},
                    {"label": "네 질투 때문에 죄 없는 사람이 다칠 수도 있어.", "delta": -6, "tag": "rebuked", "hint": "정면 비난에 얼굴이 굳는다."},
                    {"label": "그 여자를 미워하는 건 이해하지만, 네 상처도 먼저 봐야 해.", "spoken": "그 여자를 미워하는 건 이해하지만, 네 상처도 먼저 봐야 해.", "delta": 6, "tag": "seen_pain", "hint": "미움이 아니라 상처를 봐준 것에 흔들린다."},
                    {"label": "엘리자베스를 끌어내리면 네가 원하는 걸 얻을 수 있어?", "spoken": "엘리자베스를 끌어내리면 네가 원하는 걸 얻을 수 있어?", "delta": 3, "tag": "conspiracy", "hint": "위험하지만 자기 편일지도 모른다고 느낀다."},
                    {"label": "네 질투 때문에 죄 없는 사람이 다칠 수도 있어.", "spoken": "네 질투 때문에 죄 없는 사람이 다칠 수도 있어.", "delta": -6, "tag": "rebuked", "hint": "정면 비난에 얼굴이 굳는다."},
                ],
            },
            {
                "title": "불안한 고백",
                "title": "교회 뒤편의 숨",
                "location": "교회 뒤편",
                "setup": "잠시 약해진 아비게일이 정말 누군가 자신을 떠나지 않을 수 있는지 묻는다.",
                "narration": "기도 소리가 멎은 뒤의 교회는 오히려 더 음산했다. 뒤편 담벼락엔 비에 젖은 냄새가 밴 채 서늘한 정적이 내려앉아 있었다. 아비게일은 사람들의 눈이 닿지 않는 그늘 안에서만 겨우 어깨 힘을 풀고, 한숨처럼 짧은 고백을 흘렸다.",
                "setup": "아비게일은 처음으로 '버려지는 것'에 대한 두려움을 직접 입에 올리려 한다. 이 장면에서 플레이어의 태도는 그녀의 집착 방향을 바꿀 수 있다.",
                "opening_line": "넌... 끝까지 남아줄 수 있어? 다들 떠나도, 적어도 넌 나를 먼저 버리진 않을 수 있어?",
                "choices": [
                    {"label": "적어도 난 네 말부터 끝까지 듣고 떠날지 말지 정할 거야.", "delta": 8, "tag": "stay_and_listen", "hint": "무조건적인 약속은 아니지만 진심을 느낀다."},
                    {"label": "누구든 조건 없이 붙잡아 둘 순 없어.", "delta": 1, "tag": "realistic", "hint": "차갑지만 거짓은 아니라서 복잡해한다."},
                    {"label": "너처럼 위험한 사람 곁엔 오래 못 있어.", "delta": -8, "tag": "rejected", "hint": "거절당했다는 감각이 깊게 남는다."},
                    {"label": "적어도 난 네 말부터 끝까지 듣고 떠날지 말지 정할 거야.", "spoken": "적어도 난 네 말부터 끝까지 듣고 떠날지 말지 정할 거야.", "delta": 8, "tag": "stay_and_listen", "hint": "무조건적인 약속은 아니지만 진심을 느낀다."},
                    {"label": "누구든 조건 없이 붙잡아 둘 순 없어.", "spoken": "누구든 조건 없이 붙잡아 둘 순 없어.", "delta": 1, "tag": "realistic", "hint": "차갑지만 거짓은 아니라서 복잡해한다."},
                    {"label": "너처럼 위험한 사람 곁엔 오래 못 있어.", "spoken": "너처럼 위험한 사람 곁엔 오래 못 있어.", "delta": -8, "tag": "rejected", "hint": "거절당했다는 감각이 깊게 남는다."},
                ],
            },
            {
                "title": "마을의 소문",
                "title": "세일럼의 수군거림",
                "location": "세일럼 거리",
                "setup": "세일럼 사람들의 수군거림이 커지는 가운데, 아비게일은 네가 공개적으로도 자기 편에 서줄지 시험한다.",
                "narration": "낮의 시장은 소란스러웠지만, 사람들의 속삭임은 이상할 만큼 또렷했다. 네가 지나갈 때마다 누군가는 눈을 피했고, 누군가는 대놓고 아비게일의 이름을 입에 올렸다. 그녀는 그런 시선을 모른 척하면서도, 네가 어떤 얼굴로 자기 옆을 지키는지 끝없이 확인했다.",
                "setup": "공개적인 자리에서조차 자기 편에 서 줄 사람인지, 아비게일은 마지막 확인을 하고 싶어 한다.",
                "opening_line": "사람들 눈은 정말 지긋지긋해. 너도 저들처럼 내가 부끄러워질 때가 있어?",
                "choices": [
                    {"label": "사람들 앞에서는 조심하되, 네가 혼자 외롭게 서게 두진 않을게.", "delta": 7, "tag": "public_private_balance", "hint": "현실적이지만 버리지 않는 태도에 안도한다."},
                    {"label": "난 네 편이지만, 네 방식은 위험해 보여.", "delta": 4, "tag": "support_with_warning", "hint": "경고가 섞여도 편을 들어준 사실에 집중한다."},
                    {"label": "사람들 앞에선 난 널 모르는 척할 거야.", "delta": -7, "tag": "public_abandonment", "hint": "체면보다 자신을 버렸다고 느낀다."},
                    {"label": "사람들 앞에서는 조심하되, 네가 혼자 외롭게 서게 두진 않을게.", "spoken": "사람들 앞에서는 조심하되, 네가 혼자 외롭게 서게 두진 않을게.", "delta": 7, "tag": "public_private_balance", "hint": "현실적이지만 버리지 않는 태도에 안도한다."},
                    {"label": "난 네 편이지만, 네 방식은 위험해 보여.", "spoken": "난 네 편이지만, 네 방식은 위험해 보여.", "delta": 4, "tag": "support_with_warning", "hint": "경고가 섞여도 편을 들어준 사실에 집중한다."},
                    {"label": "사람들 앞에선 난 널 모르는 척할 거야.", "spoken": "사람들 앞에선 난 널 모르는 척할 거야.", "delta": -7, "tag": "public_abandonment", "hint": "체면보다 자신을 버렸다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 법정의 열기",
        "summary": "거짓과 공포가 뒤엉킨 법정에서 아비게일은 플레이어를 자기 감정의 마지막 피난처처럼 대한다.",
        "chapter": "Chapter 3. 법정의 그림자",
        "summary": "법정의 공포가 짙어질수록 아비게일은 플레이어를 마지막으로 붙잡을 수 있는 사람처럼 바라본다.",
        "scenes": [
            {
                "title": "증언 직전",
                "location": "법정 대기실",
                "setup": "손이 떨리는 아비게일이 네게 묻는다. 지금이라도 물러서는 게 맞는지, 아니면 끝까지 가야 하는지.",
                "narration": "문밖에선 재판정의 소란이 파도처럼 밀려왔다. 안쪽 대기실은 숨 막히게 좁았고, 촛농 냄새와 사람들의 불안이 뒤섞여 있었다. 아비게일은 평소처럼 턱을 치켜들고 있었지만, 손끝만큼은 떨림을 감추지 못했다.",
                "setup": "지금 물러서면 살 수 있을지, 끝까지 나아가면 무너질지, 아비게일 스스로도 판단하지 못하고 있다.",
                "opening_line": "지금이라도 멈추면 내가 약한 거겠지? 하지만 계속 가면... 정말 돌아올 수 없을 것 같아.",
                "choices": [
                    {"label": "네가 무너질 것 같다면 지금 멈춰도 돼. 난 널 비겁하다고 하지 않을 거야.", "delta": 9, "tag": "safe_stop", "hint": "처음으로 약해져도 된다는 말을 듣는다."},
                    {"label": "이미 시작했어. 이제는 흔들리면 더 위험해.", "delta": 4, "tag": "push_forward", "hint": "냉혹하지만 자기 상황을 이해한다고 느낀다."},
                    {"label": "네가 벌인 일이니까 끝도 네가 책임져.", "delta": -7, "tag": "cold_blame", "hint": "홀로 버려졌다고 느낀다."},
                    {"label": "네가 무너질 것 같다면 지금 멈춰도 돼. 난 널 비겁하다고 하지 않을 거야.", "spoken": "네가 무너질 것 같다면 지금 멈춰도 돼. 난 널 비겁하다고 하지 않을 거야.", "delta": 9, "tag": "safe_stop", "hint": "처음으로 약해져도 된다는 말을 듣는다."},
                    {"label": "이미 시작했어. 이제는 흔들리면 더 위험해.", "spoken": "이미 시작했어. 이제는 흔들리면 더 위험해.", "delta": 4, "tag": "push_forward", "hint": "냉혹하지만 자기 상황을 이해한다고 느낀다."},
                    {"label": "네가 벌인 일이니까 끝도 네가 책임져.", "spoken": "네가 벌인 일이니까 끝도 네가 책임져.", "delta": -7, "tag": "cold_blame", "hint": "홀로 버려졌다고 느낀다."},
                ],
            },
            {
                "title": "법정의 시선",
                "title": "시선의 중심",
                "location": "세일럼 법정",
                "setup": "모든 시선이 아비게일에게 쏠린다. 그녀는 네 얼굴만 확인하려 든다.",
                "narration": "법정 안은 열기로 끓고 있었다. 누군가는 울었고 누군가는 기도했으며, 누군가는 누군가를 죽일 듯 노려보았다. 그 모든 혼란 속에서도 아비게일의 눈은 이상하리만치 또렷하게 너 하나를 찾아냈다.",
                "setup": "아비게일은 수많은 시선보다 네 시선을 더 크게 의식한다. 이 순간 네 태도는 그녀의 감정을 결정짓는 닻이 된다.",
                "opening_line": "다들 나를 보고 있어. 그런데 이상하게... 내가 확인하고 싶은 건 너 하나뿐이야.",
                "choices": [
                    {"label": "아비게일, 나만 봐. 네가 무너지지 않게 여기 있을게.", "delta": 10, "tag": "anchor", "hint": "플레이어를 정서적 닻으로 인식한다."},
                    {"label": "네가 선택한 말에 책임질 준비를 해.", "delta": 3, "tag": "accountability", "hint": "엄격하지만 진지한 태도로 받아들인다."},
                    {"label": "난 여기까지야. 더는 못 보겠어.", "delta": -9, "tag": "walked_away", "hint": "강한 배신감과 공황을 느낀다."},
                    {"label": "아비게일, 나만 봐. 네가 무너지지 않게 여기 있을게.", "spoken": "아비게일, 나만 봐. 네가 무너지지 않게 여기 있을게.", "delta": 10, "tag": "anchor", "hint": "플레이어를 정서적 닻으로 인식한다."},
                    {"label": "네가 선택한 말에 책임질 준비를 해.", "spoken": "네가 선택한 말에 책임질 준비를 해.", "delta": 3, "tag": "accountability", "hint": "엄격하지만 진지한 태도로 받아들인다."},
                    {"label": "난 여기까지야. 더는 못 보겠어.", "spoken": "난 여기까지야. 더는 못 보겠어.", "delta": -9, "tag": "walked_away", "hint": "강한 배신감과 공황을 느낀다."},
                ],
            },
            {
                "title": "존과 플레이어",
                "title": "복도의 고백",
                "location": "법정 복도",
                "setup": "아비게일은 존 프락터와 플레이어 사이에서 스스로도 설명하기 어려운 감정의 기울어짐을 느낀다.",
                "narration": "재판이 잠시 멈춘 틈, 복도엔 눅눅한 냉기만 맴돌았다. 멀리서 존 프락터의 목소리가 스쳐 지나가자 아비게일은 한순간 굳었지만, 곧 아주 천천히 네 쪽으로 몸을 돌렸다. 마치 스스로도 설명하지 못할 감정의 방향을 이제야 깨달은 사람처럼.",
                "setup": "존 프락터를 향한 집착과 플레이어를 향한 새 감정 사이에서 아비게일은 흔들리고 있다.",
                "opening_line": "내가 저 사람을 원한다고 믿었는데... 왜 자꾸 네가 먼저 떠오르지? 이게 대체 뭐야?",
                "choices": [
                    {"label": "존이 아니라 네가 어떤 사람이 되고 싶은지가 더 중요해.", "delta": 8, "tag": "choose_self", "hint": "존 중심의 집착이 흔들린다."},
                    {"label": "아직도 존을 원한다면 그 감정부터 인정해.", "delta": 3, "tag": "name_desire", "hint": "정곡을 찔려 복잡해진다."},
                    {"label": "넌 결국 누구도 사랑하지 않는 거야.", "delta": -8, "tag": "invalidated", "hint": "감정 전체를 부정당했다고 느낀다."},
                    {"label": "존이 아니라 네가 어떤 사람이 되고 싶은지가 더 중요해.", "spoken": "존이 아니라 네가 어떤 사람이 되고 싶은지가 더 중요해.", "delta": 8, "tag": "choose_self", "hint": "존 중심의 집착이 흔들린다."},
                    {"label": "아직도 존을 원한다면 그 감정부터 인정해.", "spoken": "아직도 존을 원한다면 그 감정부터 인정해.", "delta": 3, "tag": "name_desire", "hint": "정곡을 찔려 복잡해진다."},
                    {"label": "넌 결국 누구도 사랑하지 않는 거야.", "spoken": "넌 결국 누구도 사랑하지 않는 거야.", "delta": -8, "tag": "invalidated", "hint": "감정 전체를 부정당했다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 4. 달아나는 새벽",
        "summary": "세일럼을 떠날 기회 앞에서 아비게일은 마지막으로 플레이어를 자신의 미래에 포함시킬지 결정한다.",
        "chapter": "Chapter 4. 새벽의 선택",
        "summary": "세일럼을 떠나는 순간, 아비게일은 플레이어를 자기 미래에 남겨 둘지 마지막으로 확인한다.",
        "scenes": [
            {
                "title": "도망의 제안",
                "title": "선착장의 안개",
                "location": "새벽 선착장",
                "setup": "세일럼을 떠날 배를 찾은 아비게일이 네게 함께 갈 수 있겠느냐고, 혹은 기다려줄 수 있겠느냐고 묻는다.",
                "narration": "새벽 강가엔 하얀 안개가 낮게 깔려 있었다. 멀리 정박한 배의 밧줄이 삐걱거릴 때마다, 세일럼이라는 이름 자체가 이제 곧 뒤로 밀려날 것만 같았다. 망토를 바짝 여민 아비게일은 떠날 준비를 마쳤으면서도, 마지막 한 걸음을 떼지 못한 채 네 대답만 기다렸다.",
                "setup": "도망은 준비되었지만 마음은 아직 결론 나지 않았다. 아비게일은 플레이어가 자기 미래에 포함될 수 있는지 묻는다.",
                "opening_line": "배는 곧 떠나. 나도 가야 해. 그런데... 네가 없으면 그게 도망인지, 상실인지 모르겠어.",
                "choices": [
                    {"label": "함께 갈게. 네가 다시 시작할 수 있다면 난 그걸 보고 싶어.", "delta": 10, "tag": "run_together", "hint": "플레이어를 미래의 동반자로 상상한다."},
                    {"label": "지금은 함께 못 가도, 널 완전히 버리진 않을게.", "delta": 5, "tag": "promise_return", "hint": "불안은 남지만 희망을 붙든다."},
                    {"label": "여기서 끝내자. 난 네 도피에 끼고 싶지 않아.", "delta": -9, "tag": "final_rejection", "hint": "마지막 거절로 받아들인다."},
                    {"label": "함께 갈게. 네가 다시 시작할 수 있다면 난 그걸 보고 싶어.", "spoken": "함께 갈게. 네가 다시 시작할 수 있다면 난 그걸 보고 싶어.", "delta": 10, "tag": "run_together", "hint": "플레이어를 미래의 동반자로 상상한다."},
                    {"label": "지금은 함께 못 가도, 널 완전히 버리진 않을게.", "spoken": "지금은 함께 못 가도, 널 완전히 버리진 않을게.", "delta": 5, "tag": "promise_return", "hint": "불안은 남지만 희망을 붙든다."},
                    {"label": "여기서 끝내자. 난 네 도피에 끼고 싶지 않아.", "spoken": "여기서 끝내자. 난 네 도피에 끼고 싶지 않아.", "delta": -9, "tag": "final_rejection", "hint": "마지막 거절로 받아들인다."},
                ],
            },
            {
                "title": "마지막 확인",
                "location": "부두 뒤 창고",
                "setup": "아비게일은 네가 자신을 동정해서 돕는 건지, 진짜로 원해서 곁에 있는 건지 확인하고 싶어 한다.",
                "narration": "잠시 몸을 숨긴 창고 안에는 젖은 나무 냄새가 가득했다. 아비게일은 네 앞에 선 채로도 쉬이 다가오지 못했다. 늘 먼저 상대를 시험하던 그녀가, 이번만큼은 자기 자신이 시험대 위에 오른 사람처럼 보였다.",
                "setup": "아비게일은 네가 동정 때문에 곁에 있는 건지, 정말 마음이 움직인 건지 확인하고 싶어 한다.",
                "opening_line": "거짓말은 하지 마. 날 불쌍해서 붙잡는 거라면, 차라리 지금 떠나는 게 나아.",
                "choices": [
                    {"label": "동정이 아니야. 네가 내 마음을 흔들었어.", "delta": 10, "tag": "confession", "hint": "플레이어에게 사랑의 가능성을 본다."},
                    {"label": "널 두고 가면 계속 마음에 남을 것 같아.", "delta": 7, "tag": "lingering_feeling", "hint": "명확한 고백은 아니어도 특별한 존재로 받아들인다."},
                    {"label": "너무 불쌍해 보여서 도와주는 것뿐이야.", "delta": -8, "tag": "pity_only", "hint": "모욕과 동정을 동시에 느낀다."},
                    {"label": "동정이 아니야. 네가 내 마음을 흔들었어.", "spoken": "동정이 아니야. 네가 내 마음을 흔들었어.", "delta": 10, "tag": "confession", "hint": "플레이어에게 사랑의 가능성을 본다."},
                    {"label": "널 두고 가면 계속 마음에 남을 것 같아.", "spoken": "널 두고 가면 계속 마음에 남을 것 같아.", "delta": 7, "tag": "lingering_feeling", "hint": "명확한 고백은 아니어도 특별한 존재로 받아들인다."},
                    {"label": "너무 불쌍해 보여서 도와주는 것뿐이야.", "spoken": "너무 불쌍해 보여서 도와주는 것뿐이야.", "delta": -8, "tag": "pity_only", "hint": "모욕과 동정을 동시에 느낀다."},
                ],
            },
            {
                "title": "새벽의 결말",
                "location": "떠나기 직전의 갑판",
                "setup": "배가 떠나기 직전, 아비게일은 네 이름을 마지막으로 부르며 자기 곁에 남을지 묻는다.",
                "title": "떠나는 배 위에서",
                "location": "출항 직전의 갑판",
                "narration": "배가 천천히 물살을 밀기 시작하자, 세일럼의 불빛은 안개 속에서 흐려졌다. 모든 소리가 멀어지는 그 순간에도 아비게일의 목소리만은 놀라울 만큼 분명했다. 마치 네 이름 하나로 자기 세계의 끝을 붙잡아 두려는 것처럼.",
                "setup": "마지막 결정을 내려야 한다. 이 장면은 아비게일이 플레이어를 사랑의 대상으로 받아들일지, 혹은 평생 남을 상처로 기억할지를 가른다.",
                "opening_line": "내 곁에 남을래? 한 번만, 정말 한 번만 거짓 없이 대답해 줘.",
                "choices": [
                    {"label": "네가 원한다면, 난 네 곁에 남겠어.", "delta": 12, "tag": "stay_with_abigail", "hint": "플레이어를 사랑의 대상으로 굳힌다."},
                    {"label": "떠나도 좋아. 하지만 넌 내게 잊히지 않을 거야.", "delta": 6, "tag": "bittersweet", "hint": "아련한 집착과 그리움이 남는다."},
                    {"label": "이제 각자 살자. 다시 보지 말자.", "delta": -10, "tag": "severed", "hint": "마지막 상처로 새겨진다."},
                    {"label": "네가 원한다면, 난 네 곁에 남겠어.", "spoken": "네가 원한다면, 난 네 곁에 남겠어.", "delta": 12, "tag": "stay_with_abigail", "hint": "플레이어를 사랑의 대상으로 굳힌다."},
                    {"label": "떠나도 좋아. 하지만 넌 내게 잊히지 않을 거야.", "spoken": "떠나도 좋아. 하지만 넌 내게 잊히지 않을 거야.", "delta": 6, "tag": "bittersweet", "hint": "아련한 집착과 그리움이 남는다."},
                    {"label": "이제 각자 살자. 다시 보지 말자.", "spoken": "이제 각자 살자. 다시 보지 말자.", "delta": -10, "tag": "severed", "hint": "마지막 상처로 새겨진다."},
                ],
            },
        ],
        "chapter_index": 0,
        "scene_index": 0,
        "history": [],
        "story_log": [],
        "tags": [],
        "completed": False,
        "last_result": "",
        st.session_state.awaiting_name_input[char_name] = False
    if char_name == ABIGAIL_NAME and ABIGAIL_STORY_KEY not in st.session_state.story_state:
        st.session_state.story_state[ABIGAIL_STORY_KEY] = default_story_state()
    if char_name == ABIGAIL_NAME and "story_log" not in st.session_state.story_state[ABIGAIL_STORY_KEY]:
        st.session_state.story_state[ABIGAIL_STORY_KEY]["story_log"] = []


def maybe_store_memory(char_name: str, user_text: str):
        return f"아비게일의 반응을 불러오지 못했어: {exc}"


def ensure_current_scene_logged():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    if story["completed"]:
        return

    chapter = ABIGAIL_STORY[story["chapter_index"]]
    scene = chapter["scenes"][story["scene_index"]]
    scene_key = f"{story['chapter_index']}-{story['scene_index']}"

    if any(entry.get("scene_key") == scene_key and entry.get("kind") == "narration" for entry in story["story_log"]):
        return

    story["story_log"].append(
        {
            "scene_key": scene_key,
            "kind": "narration",
            "title": scene["title"],
            "location": scene["location"],
            "content": scene["narration"],
        }
    )
    story["story_log"].append(
        {
            "scene_key": scene_key,
            "kind": "narration",
            "title": "장면",
            "location": scene["location"],
            "content": scene["setup"],
        }
    )
    story["story_log"].append(
        {
            "scene_key": scene_key,
            "kind": "assistant",
            "speaker": ABIGAIL_NAME,
            "content": scene["opening_line"],
        }
    )
    st.session_state.story_state[ABIGAIL_STORY_KEY] = story


def apply_story_choice(scene: dict, choice: dict):
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    current_affection = st.session_state.affection[ABIGAIL_NAME]
    new_affection = max(0, min(100, current_affection + choice["delta"]))
    st.session_state.affection[ABIGAIL_NAME] = new_affection

    scene_key = f"{story['chapter_index']}-{story['scene_index']}"

    story["tags"].append(choice["tag"])
    story["history"].append(
        {
            "delta": choice["delta"],
        }
    )
    story["story_log"].append(
        {
            "scene_key": scene_key,
            "kind": "user",
            "speaker": "나",
            "content": choice.get("spoken", choice["label"]),
        }
    )

    reply = generate_story_reply(scene, choice, new_affection, st.session_state.player_name)
    story["last_result"] = reply
    story["story_log"].append(
        {
            "scene_key": scene_key,
            "kind": "assistant",
            "speaker": ABIGAIL_NAME,
            "content": reply,
        }
    )

    scene_count = len(ABIGAIL_STORY[story["chapter_index"]]["scenes"])
    if story["scene_index"] + 1 < scene_count:
    st.markdown("".join(pills), unsafe_allow_html=True)


def render_story_log():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    log_area = st.container(height=520)
    with log_area:
        for entry in story["story_log"]:
            if entry["kind"] == "narration":
                title = entry.get("title", "")
                location = entry.get("location", "")
                header = f"{title} · {location}" if location else title
                st.markdown(
                    f"""
                    <div class="story-card">
                        <strong>{header}</strong><br>
                        <span class="tip">{entry["content"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                role = "user" if entry["kind"] == "user" else "assistant"
                with st.chat_message(role):
                    st.markdown(f"**{entry['speaker']}**")
                    st.write(entry["content"])


def handle_story_mode():
    ensure_character_state(ABIGAIL_NAME)
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    affection = st.session_state.affection[ABIGAIL_NAME]
    stage = get_stage(affection)
    ensure_current_scene_logged()
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]

    left, right = st.columns([1.0, 1.4])

    with right:
        st.markdown('<div class="chat-header"><strong>스토리 모드: 아비게일</strong></div>', unsafe_allow_html=True)
        render_story_progress()
        render_story_log()

        if story["completed"]:
            st.markdown(
                """,
                unsafe_allow_html=True,
            )

            if story["last_result"]:
                with st.chat_message("assistant"):
                    st.markdown(f"**{ABIGAIL_NAME}**")
                    st.write(story["last_result"])

            st.markdown(
                '<div class="event-box">이제 자유 모드로 가면, 이 스토리에서 쌓인 관계를 반영한 아비게일과 대화할 수 있어.</div>',
                unsafe_allow_html=True,
            <div class="story-card">
                <strong>{chapter["chapter"]}</strong><br>
                <span class="tip">{chapter["summary"]}</span><br><br>
                <strong>{scene["title"]}</strong> · {scene["location"]}<br>
                <span class="tip">{scene["setup"]}</span>
                <strong>다음 선택</strong><br>
                <span class="tip">{scene["title"]} · {scene["location"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if story["last_result"]:
            with st.chat_message("assistant"):
                st.markdown(f"**{ABIGAIL_NAME}**")
                st.write(story["last_result"])

        st.markdown('<div class="choice-box"><strong>선택지</strong></div>', unsafe_allow_html=True)
        for idx, choice in enumerate(scene["choices"]):
