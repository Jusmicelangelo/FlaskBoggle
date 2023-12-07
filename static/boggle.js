class BoggleGame {

    constructor() {
        this.gameLength = 60;
        this.showTimer();
        this.score = 0;
        this.wordList = new Set()
        this.timer = setInterval(this.second.bind(this), 1000);
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    countScore() {
        $(".score")
          .text(this.score)
    }

    notification(msg) {
        $(".msg")
          .text(msg)
      }

    // taking the guess input

    async handleSubmit (evt) {
        evt.preventDefault();
        const $word = $(".guess");
        let word = $word.val().toLowerCase();
        if (!word) return;
        if (this.wordList.has(word)) {
            this.notification(`Already guessed ${word}`);
            return;
        }
   
        // sending word to server to check

        const resp = await axios.get("/word-check", { params: { "word": word }})
        let result = resp.data.result
        alert(result)
        if (resp.data.result === "not-word") {
            this.notification(`${word} is not a valid English word`);
        } 
        else if (resp.data.result === "not-on-board") {
            this.notification(`${word} is not a valid word on this board`);
        } 
        else {
            this.notification(`Added: ${word}`);
            this.wordList.add(word)
            this.score += word.length
            this.countScore()
        }
    }

    showTimer() {
        $(".timer")
          .text(this.gameLength)
    }
    // ticking one second and disabling form when timer is over
    async second() {
        this.gameLength -= 1;
        this.showTimer();
        if (this.gameLength === 0) {
            clearInterval(this.timer);
            $(".guess").prop("disabled", true);
            await this.gameEnd()
          }
    }

    async gameEnd() {
        // sending score to server to compare to highscore
        const resp = await axios.post("/end-game", { score: this.score });
        if (resp.data.record) {
            this.notification(`New all time record: ${this.score}`);
        } 
        else {
            this.notification(`Final score: ${this.score}`);
        } 
    }
}