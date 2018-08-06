# r/RoguelikeDev Tutorial 2018

![RoguelikeDev Does the Complete Roguelike Tutorial Event Logo](https://i.imgur.com/EYJFgdI.png)

At [r/roguelikedev](https://reddit.com/r/roguelikedev/wiki/python_tutorial_series) we're doing a dev-along following [The Complete Roguelike Tutorial.](http://rogueliketutorials.com/libtcod/1) Come and check this out!

I'll be diverging a bit from the main Python tutorial by implementing Esper's entity component system. I'll be also using python-tcod for it's new console class, and numpy arrays for the game map. 
 
## Current Features
* Contains over 50 classic roguelike [monsters](https://github.com/toptea/roguelike_tutorial/blob/master/src/data/monster.csv)
* 20 different kind of [items](https://github.com/toptea/roguelike_tutorial/blob/master/src/data/item.csv) (all throwable)
* Able to generate 4 different map types: 
  * [irregular rooms](https://i.imgur.com/1gbj1dc.png)
  * [long passageway](https://i.imgur.com/NERgrGl.png)
  * [monster nest](https://i.imgur.com/5KcPg7g.png)
  * [large opening](https://i.imgur.com/3n5KsJY.png)
* Support 3 [input configurations](http://www.roguebasin.com/index.php?title=User_interface_features#Movement_keys) for player movement:
  * arrow keys (Infra Arcana style, ctrl/shift for diagonal movement)
  * vi keys
  * numpad
 
## Useful Links
* [ecs dependency matrix for this game](https://docs.google.com/spreadsheets/d/1VBtESOR2Gw8qIozxbZZv7mtPuL6ecgKIm38q0Ai-ZSg/edit#gid=0)
* [dataclass](https://kotlinfrompython.wordpress.com/2018/04/30/python-dataclasses-a-revolution/) - a new way of defining class in Python 3.7
* [python-tcod](http://python-tdl.readthedocs.io/en/latest/?badge=latest) - python libtcod documentation
* [libtcod](http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/index2.html) - original libtcod documentation
* [numpy](https://docs.scipy.org/doc/numpy-1.14.0/index.html) - multi-dimensional array
* [skimage](http://scikit-image.org/docs/stable/api/skimage.draw.html) - various algorithm shapes
* [esper](https://github.com/benmoran56/esper) - entity component system

## If you would like to participate 

* [Sign up for a free personal account](https://gitlab.com/users/sign_in#register-pane) if you don't already have one.
* Fork [this repository](https://gitlab.com/aaron-santos/roguelikedev-does-the-complete-roguelike-tutorial) to your account.
* Clone the repository on your computer and follow the tutorial.
* Follow along with the [weekly posts](https://www.reddit.com/r/roguelikedev).
* Update the `README.md` file to include a description of your game, how/where to play/download it, how to build/compile it, what dependencies it has, etc.
* Share your game on the final week.

## It's dangerous to go alone

If you're **new to Git or version control**…

* [Git Documentation](https://git-scm.com/documentation) - everything you need to know about version control, and how to get started with Git.
* [GitHub](https://help.github.com/)/[GitLab](https://gitlab.com/help/gitlab-basics/command-line-commands.md#start-working-on-your-project) - start working on your project.
