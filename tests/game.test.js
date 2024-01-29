import { Game, make2DBoard } from "../static/game.js";
import { test, expect, jest } from "@jest/globals";

test("create a Game object without problem", () => {
	const game = new Game();

	expect(game).toBeDefined();
});

test("get cell length from the Game object", () => {
	const game = new Game(100);

	expect(game.getCellLength()).toBe(100);
});

test("Game has the correct canvas width", () => {
	const game = new Game(100);
	const biggerGame = new Game(150);

	expect(game.getCanvasWidth()).toBe(700);
	expect(biggerGame.getCanvasWidth()).toBe(1050);
});

test("Game has the correct canvas height", () => {
	const game = new Game(100);
	const biggerGame = new Game(150);

	expect(game.getCanvasHeight()).toBe(800);
	expect(biggerGame.getCanvasHeight()).toBe(1200);
});

test("all cell should be emptied on start", () => {
	const game = new Game(100);

	for (var i = 0; i < 6; i++) {
		for (var j = 0; j < 6; j++) {
			expect(game.getCellState(j, i)).toBe("empty");
		}
	}
});

test("drop multiple coins should stack up properly", () => {
	const game = new Game(100);

	game.dropCoin(0);
	game.dropCoin(0);
	game.dropCoin(1);

	let expectedBoard = make2DBoard(6, 7);
	expectedBoard[0][0] = "player";
	expectedBoard[1][0] = "player";
	expectedBoard[0][1] = "player";
	expect(game.board).toEqual(expectedBoard);
});