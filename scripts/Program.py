import Common
import VGame


def main():
    params = Common.getParams("params.json")
    game = VGame.VGame(params)
    game.run()


if __name__ == '__main__':
    main()