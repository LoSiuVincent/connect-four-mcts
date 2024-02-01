export class Controller {
	constructor(game, view, server) {
		this.game = game;
		this.view = view;
		this.server = server;

		this.view.addListener("mouseClick", this);
	}

	async update(data) {
		await this.handleMouseClick(data.x, data.y);
	}

	async handleMouseClick(x, y) {
		if (this.view.isInsideCanvas(x, y)) {
			const colIndex = Math.floor(x / this.view.getCellLength());
			this.game.dropCoin(colIndex);
			await this.makeComputerMove();
		}
	}

	async makeComputerMove() {
		const computerMove = await this.server.getComputerMove(this._encodeBoard(this.game.board));
		this.game.dropCoin(computerMove, "computer");
	}

	_encodeBoard(board) {
		let result = "";
		for (let row of board) {
			for (let state of row) {
				let char;
				switch (state) {
					case "player":
						char = "P";
						break;
					case "computer":
						char = "C";
						break;
					case "empty":
						char = "E";
						break;
					default:
						console.error("Got unknown cell state")
				}
				result = result.concat(char);
			}
			result = result.concat("|");
		}
		result = result.slice(0, -1);
		return result;
	}
}
