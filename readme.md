https://github.com/vijayproxima/logitechai.git

## create a new repository on the command line
echo "# logitechai" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M develop
git remote add origin https://github.com/vijayproxima/logitechai.git
git push -u origin develop

## push an existing repository from the command line
git remote add origin https://github.com/vijayproxima/logitechai.git
git branch -M develop
git push -u origin develop