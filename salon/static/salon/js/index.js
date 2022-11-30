function music_button(music)
{
    document.getElementById("myAudio").pause();
    document.getElementById("myAudio").setAttribute('src', music);
    document.getElementById("myAudio").loadFile();
    document.getElementById("myAudio").play();
}