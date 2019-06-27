const tableData = {
  "seats": 6,
  "commands": [
    [
      "",
      "",
      "20 "
    ],
    [
      "",
      1.0,
      "[1] $0.02 "
    ],
    [
      "RAISE",
      2.0,
      "Raise To $0.04 "
    ]
  ],
  "cards": [
    true,
    false,
    false,
    true,
    true,
    true
  ],
  "nocards": [
    false,
    true,
    false,
    false,
    false,
    false
  ],
  "button": [
    false,
    false,
    false,
    false,
    true,
    false
  ],
  "flop": [
    "",
    "",
    "",
    "",
    "",
    ""
  ],
  "hero": {
    "hero_cards": "8h6s",
    "position": "MP",
    "hero_pos": 3
  },
  "hand_analisys": {
    "hand_phase": "PREFLOP",
    "result": [
      [
        "8h6s:XX",
        0.4318955
      ]
    ]
  },
  "decision": {
    "decision": "FOLD OR CHECK",
    "raise_strategy": "0"
  },
  "command": {
    "to_execute": 0
  },
  "image_platform": "POKERSTARS",
  "image_tabletype": "6-SEATS"
};


export default function getTableData(){
  return tableData;
}

