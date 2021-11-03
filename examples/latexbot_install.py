from codebots.bots import LatexBot

lbot = LatexBot()
lbot.install_dependencies(git=False, pandoc=True, miktex=True)
