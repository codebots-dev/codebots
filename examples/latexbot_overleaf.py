from codebots.bots import LatexBot

lbot = LatexBot()

# change the placeholder with your document code: you can find in the address bar
# in your browser when you open the overleaf project.

lbot.convert_overleaf_to_docx("XXXXXXXXXXXXXX", upload=True)
