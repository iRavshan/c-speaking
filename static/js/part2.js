let startingMinutes = 0;
let startingSeconds = 0;
let time = 0;
const countdownEl = document.getElementById('timer');
const signalAudio = document.getElementById('signalAudio');
var questionAudio = document.getElementById('questionAudio');
const infoAudio = document.getElementById('infoAudio');
const practicePanel = document.getElementById('practice-panel');
const resultPanel = document.getElementById('result-panel');
const infoText = document.getElementById('infoText');
var question = document.getElementById('question');
var answers = document.getElementsByName('answer');
let repetitions = 0;
const totalRepetitions = 1;
let isPreparation = true;
const timer = 0;

let mediaRecorder;
let audioChunks = [];

function setTimer(minutes, seconds){
    startingMinutes = minutes;
    startingSeconds = seconds;
    time = startingMinutes * 60 + startingSeconds;
}

function playSignal(){
    signalAudio.play();
}

function playQuestion(){
    questionAudio.play();
    
    questionAudio.onended = function() {
        isPreparation = true;
        setTimer(1, 0);
        timer = setInterval(updateCountdown, 1000)
    }
}

function playInfo(){
    infoAudio.play();

    infoAudio.onended = function() {
        infoText.style.display = 'none';
        showQuestion();
        playQuestion();
    };
}

function showQuestion(){
    question.style.display = 'block';
}

playInfo();

function updateCountdown() {
    let minutes = Math.floor(time / 60);
    let seconds = time % 60;
    minutes = minutes < 10 ? '0' + minutes: minutes;
    seconds = seconds < 10 ? '0' + seconds: seconds;
    countdownEl.innerHTML = `${minutes}:${seconds}`;

    if (time == 0){
        if(totalRepetitions === repetitions){
            clearInterval(timer);
            stopRecording();
            practicePanel.style.display = 'none';
            resultPanel.style.display = 'block';
        }
        else if(isPreparation === true){
                playSignal();
                startRecording();
                repetitions++;
                setTimer(2, 0);
                isPreparation = false;
            }
            else{
                stopRecording();
                setTimer(0, 0);
                isPreparation = true;
            }
    }
    else{
        time--;        
    }
}

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        answers[repetitions-1].src = audioUrl;
        audioChunks = [];
    };

    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
}