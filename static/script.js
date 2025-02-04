let storyElement = document.getElementById("story");

function sendPrediction(input, callback) {
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: input })
    })
    .then(response => response.json())
    .then(data => {
        callback(data.output);
    })
    .catch(error => console.error('Error:', error));
}

let scenes = {
    start: {
        text: "خوش آمدید به بازی ماجراجویی متنی! شما در جنگل گم شده‌اید. چه کاری انجام می‌دهید؟",
        choices: [
            { text: "به سمت چپ بروید", nextScene: "left" },
            { text: "به سمت راست بروید", nextScene: "right" },
            { text: "به راه خود ادامه دهید", nextScene: "forward" }
        ]
    },
    left: {
        text: "شما به یک رودخانه رسیدید. چه کاری انجام می‌دهید؟",
        choices: [
            { text: "از رودخانه عبور کنید", nextScene: "crossRiver" },
            { text: "کنار رودخانه قدم بزنید", nextScene: "walkByRiver" },
            { text: "به عقب برگردید", nextScene: "start" }
        ]
    },
    right: {
        text: "شما به یک غار رسیدید. چه کاری انجام می‌دهید؟",
        choices: [
            { text: "وارد غار شوید", nextScene: "enterCave" },
            { text: "اطراف غار جستجو کنید", nextScene: "exploreCave" },
            { text: "به عقب برگردید", nextScene: "start" }
        ]
    },
    forward: {
        text: "شما به یک جنگل تاریک رسیدید. چه کاری انجام می‌دهید؟",
        choices: [
            { text: "وارد جنگل شوید", nextScene: "enterForest" },
            { text: "به عقب برگردید", nextScene: "start" },
            { text: "به چپ بپیچید", nextScene: "left" }
        ]
    },
    crossRiver: {
        text: "شما از رودخانه عبور کردید و یک روستای زیبا پیدا کردید. بازی تمام شد!",
        choices: []
    },
    walkByRiver: {
        text: "شما کنار رودخانه قدم زدید و به یک آبشار زیبا رسیدید. بازی تمام شد!",
        choices: []
    },
    enterCave: {
        text: "شما وارد غار شدید و یک گنج بزرگ پیدا کردید. بازی تمام شد!",
        choices: []
    },
    exploreCave: {
        text: "شما اطراف غار جستجو کردید و یک نقشه‌ی گنج پیدا کردید. بازی تمام شد!",
        choices: []
    },
    enterForest: {
        text: "شما وارد جنگل تاریک شدید و یک حیوان جنگلی دوست داشتنی پیدا کردید. بازی تمام شد!",
        choices: []
    }
};

function choose(option) {
    let scene = scenes[currentScene].choices[option - 1].nextScene;
    showScene(scene);
}

let currentScene = "start";

function showScene(scene) {
    currentScene = scene;
    let sceneData = scenes[scene];
    storyElement.innerHTML = sceneData.text;
    let choicesElement = document.getElementById("choices");
    choicesElement.innerHTML = "";
    sceneData.choices.forEach((choice, index) => {
        let button = document.createElement("button");
        button.textContent = choice.text;
        button.onclick = () => choose(index + 1);
        choicesElement.appendChild(button);
    });
}

showScene(currentScene);
