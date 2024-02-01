import { test, expect, jest } from "@jest/globals";
import { Controller } from "controller.js";
import { make2DBoard } from "game.js";

test("controller should call the correct dropCoin when receieve the mouse click event", async () => {
	const mockGame = {
		dropCoin: jest.fn(),
		board: [[]],
	};
	const mockView = {
		getCellLength: () => 100,
		addListener: () => { },
		isInsideCanvas: () => true
	};
	const mockServer = {
		getComputerMove: () => 0,
	};
	const controller = new Controller(mockGame, mockView, mockServer);

	for (let i = 0; i < 7; i++) {
		await controller.handleMouseClick(50 + 100 * i, 10);
		expect(mockGame.dropCoin).toHaveBeenCalledWith(i);
	}
});

test("controller should add itself to listen on View", () => {
	const mockGame = {};
	const mockView = { addListener: jest.fn() };
	const controller = new Controller(mockGame, mockView);

	expect(mockView.addListener).toHaveBeenCalledWith("mouseClick", controller);
})

test("controller encode board to correct string", () => {
	const mockGame = {};
	const mockView = { addListener: jest.fn() };
	const controller = new Controller(mockGame, mockView);
	const board = make2DBoard(6, 7);
	board[0][0] = "player";
	board[1][0] = "computer";

	expect(controller._encodeBoard(board)).toEqual("PEEEEEE|CEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");
})

test("controller should not make computer move when it is thinking", async () => {
	const mockGame = {
		dropCoin: jest.fn(),
		board: [[]],
	};
	const mockView = {
		getCellLength: () => 100,
		addListener: () => { },
		isInsideCanvas: () => true
	};
	const mockServer = { getComputerMove: () => 1 };
	const controller = new Controller(mockGame, mockView, mockServer);
	const spy = jest.spyOn(controller, "makeComputerMove");

	const firstPromise = controller.handleMouseClick(10, 10);
	const secondPromise = controller.handleMouseClick(10, 10);
	await secondPromise;
	await firstPromise;

	expect(spy).toHaveBeenCalledTimes(1);
})