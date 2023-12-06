class BoggleGame {

    constructor() {
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
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
        }

    }
}