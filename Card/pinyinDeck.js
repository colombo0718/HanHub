// pinyinDeck.js
// 全域變數版本：在 <script src="pinyinDeck.js"></script> 後，直接用 window.PINYIN_DECK.cards

window.PINYIN_DECK = {
  suits: {
    L: { name: "聽力", label: "Listening", icon: "👂💧" },
    S: { name: "口說", label: "Speaking",  icon: "👄🔥" },
    R: { name: "閱讀", label: "Reading",   icon: "👀🌱" },
    W: { name: "書寫", label: "Writing",   icon: "✍️🌬" }
  },

  cards: [
    // L 組：聽・水
    { suit:"L", hex:"0", main:"ˊ",   hanzi:"牙",   pinyin:"yá",       emoji:"🦷"    },
    { suit:"L", hex:"1", main:"b",   hanzi:"包",   pinyin:"bāo",      emoji:"👛"    },
    { suit:"L", hex:"2", main:"d",   hanzi:"燈",   pinyin:"dēng",     emoji:"💡"    },
    { suit:"L", hex:"3", main:"g",   hanzi:"狗",   pinyin:"gǒu",      emoji:"🐶"    },
    { suit:"L", hex:"4", main:"q",   hanzi:"球",   pinyin:"qiú",      emoji:"⚽"    },
    { suit:"L", hex:"5", main:"sh",  hanzi:"書",   pinyin:"shū",      emoji:"📖"    },
    { suit:"L", hex:"6", main:"s",   hanzi:"傘",   pinyin:"sǎn",      emoji:"☂️"    },
    { suit:"L", hex:"7", main:"i",   hanzi:"衣",   pinyin:"yī",       emoji:"👕"    },
    { suit:"L", hex:"8", main:"ei",  hanzi:"杯",   pinyin:"bēi",      emoji:"🥤"    },
    { suit:"L", hex:"9", main:"ya",  hanzi:"鴨",   pinyin:"yā",       emoji:"🦆"    },
    { suit:"L", hex:"A", main:"wa",  hanzi:"襪",   pinyin:"wà",       emoji:"🧦"    },
    { suit:"L", hex:"B", main:"ang", hanzi:"羊",   pinyin:"yáng",     emoji:"🐑"    },
    { suit:"L", hex:"C", main:"in",  hanzi:"音",   pinyin:"yīn",      emoji:"🎵"    },
    { suit:"L", hex:"D", main:"wan", hanzi:"碗",   pinyin:"wǎn",      emoji:"🍚"    },
    { suit:"L", hex:"E", main:"ün",  hanzi:"雲",   pinyin:"yún",      emoji:"☁️"    },
    { suit:"L", hex:"F", main:"en",  hanzi:"恩",   pinyin:"ēn",       emoji:"🙏"    },

    // S 組：說・火
    { suit:"S", hex:"0", main:"ˇ",   hanzi:"啞",   pinyin:"yǎ",       emoji:"🤐"    },
    { suit:"S", hex:"1", main:"p",   hanzi:"跑",   pinyin:"pǎo",      emoji:"🏃"    },
    { suit:"S", hex:"2", main:"t",   hanzi:"兔",   pinyin:"tù",       emoji:"🐰"    },
    { suit:"S", hex:"3", main:"k",   hanzi:"卡",   pinyin:"kǎ",       emoji:"💳"    },
    { suit:"S", hex:"4", main:"x",   hanzi:"洗",   pinyin:"xǐ",       emoji:"🧼"    },
    { suit:"S", hex:"5", main:"r",   hanzi:"肉",   pinyin:"ròu",      emoji:"🍖"    },
    { suit:"S", hex:"6", main:"a",   hanzi:"哈",   pinyin:"hā",       emoji:"😆"    },
    { suit:"S", hex:"7", main:"u",   hanzi:"豬",   pinyin:"zhū",      emoji:"🐷"    },
    { suit:"S", hex:"8", main:"ao",  hanzi:"貓",   pinyin:"māo",      emoji:"🐱"    },
    { suit:"S", hex:"9", main:"ie",  hanzi:"寫",   pinyin:"xiě",      emoji:"✍️"    },
    { suit:"S", hex:"A", main:"uo",  hanzi:"火",   pinyin:"huǒ",      emoji:"🔥"    },
    { suit:"S", hex:"B", main:"eng", hanzi:"冷",   pinyin:"lěng",     emoji:"🥶"    },
    { suit:"S", hex:"C", main:"iang",hanzi:"想",   pinyin:"xiǎng",    emoji:"🤔"    },
    { suit:"S", hex:"D", main:"wen", hanzi:"問",   pinyin:"wèn",      emoji:"❓"    },
    { suit:"S", hex:"E", main:"er",  hanzi:"耳",   pinyin:"ěr",       emoji:"👂"    },
    { suit:"S", hex:"F", main:"üe",  hanzi:"雪",   pinyin:"xuě",      emoji:"❄️"    },

    // R 組：讀・土
    { suit:"R", hex:"0", main:"ˋ",   hanzi:"亞",   pinyin:"yà",       emoji:"👘"    },
    { suit:"R", hex:"1", main:"m",   hanzi:"馬",   pinyin:"mǎ",       emoji:"🐴"    },
    { suit:"R", hex:"2", main:"n",   hanzi:"牛",   pinyin:"niú",      emoji:"🐮"    },
    { suit:"R", hex:"3", main:"h",   hanzi:"花",   pinyin:"huā",      emoji:"🌺"    },
    { suit:"R", hex:"4", main:"zh",  hanzi:"鐘",   pinyin:"zhōng",    emoji:"⏰"    },
    { suit:"R", hex:"5", main:"z",   hanzi:"字",   pinyin:"zì",       emoji:"🔤"    },
    { suit:"R", hex:"6", main:"o",   hanzi:"鍋",   pinyin:"guō",      emoji:"🍲"    },
    { suit:"R", hex:"7", main:"ü",   hanzi:"魚",   pinyin:"yú",       emoji:"🐟"    },
    { suit:"R", hex:"8", main:"ou",  hanzi:"口",   pinyin:"kǒu",      emoji:"👄"    },
    { suit:"R", hex:"9", main:"iao", hanzi:"小",   pinyin:"xiǎo",     emoji:"🤏"    },
    { suit:"R", hex:"A", main:"uai", hanzi:"壞",   pinyin:"huài",     emoji:"😈"    },
    { suit:"R", hex:"B", main:"ong", hanzi:"龍",   pinyin:"lóng",     emoji:"🐲"    },
    { suit:"R", hex:"C", main:"ing", hanzi:"星",   pinyin:"xīng",     emoji:"⭐"    },
    { suit:"R", hex:"D", main:"uang",hanzi:"光",   pinyin:"guāng",    emoji:"🔦"    },
    { suit:"R", hex:"E", main:"ê",   hanzi:"耶",   pinyin:"yē",       emoji:"✌️"    },
    { suit:"R", hex:"F", main:"wen", hanzi:"溫",   pinyin:"wēn",      emoji:"🌡️"    },

    // W 組：寫・風
    { suit:"W", hex:"0", main:"·",   hanzi:"呀",   pinyin:"ya",       emoji:"❗"    },
    { suit:"W", hex:"1", main:"f",   hanzi:"風",   pinyin:"fēng",     emoji:"🌬️"   },
    { suit:"W", hex:"2", main:"l",   hanzi:"籃",   pinyin:"lán",      emoji:"🧺"    },
    { suit:"W", hex:"3", main:"j",   hanzi:"雞",   pinyin:"jī",       emoji:"🐔"    },
    { suit:"W", hex:"4", main:"ch",  hanzi:"車",   pinyin:"chē",      emoji:"🚗"    },
    { suit:"W", hex:"5", main:"c",   hanzi:"菜",   pinyin:"cài",      emoji:"🥬"    },
    { suit:"W", hex:"6", main:"e",   hanzi:"鵝",   pinyin:"é",        emoji:"🦢"    },
    { suit:"W", hex:"7", main:"ai",  hanzi:"愛",   pinyin:"ài",       emoji:"❤️"    },
    { suit:"W", hex:"8", main:"an",  hanzi:"山",   pinyin:"shān",     emoji:"⛰️"    },
    { suit:"W", hex:"9", main:"you", hanzi:"油",   pinyin:"yóu",      emoji:"🛢️"    },
    { suit:"W", hex:"A", main:"ui",  hanzi:"對",   pinyin:"duì",      emoji:"✔️"    },
    { suit:"W", hex:"B", main:"ian", hanzi:"錢",   pinyin:"qián",     emoji:"💰"    },
    { suit:"W", hex:"C", main:"iong",hanzi:"熊",   pinyin:"xióng",    emoji:"🐻"    },
    { suit:"W", hex:"D", main:"uan", hanzi:"拳",   pinyin:"quán",     emoji:"👊"    },
    { suit:"W", hex:"E", main:"yo",  hanzi:"喲",   pinyin:"yo",       emoji:"😮"    },
    { suit:"W", hex:"F", main:"wei", hanzi:"圍",   pinyin:"wéi",      emoji:"🧣"    }
  ]
};
