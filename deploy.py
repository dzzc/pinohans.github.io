import os


class Deploy:
    def __init__(self) -> None:
        self.clean()
        self.generator()
        self.deploy()

    def generator(self) -> str:
        def walk(root: str) -> str:
            # 当前目录的所有文件夹项
            dir = ''
            # 当前目录的所有文件项
            file = ''
            for child in os.listdir(root):
                childpath = os.path.join(root, child)
                if os.path.isdir(childpath) and not child.startswith('.'):
                    # 获得子目录的所有文件夹、文件项
                    childdirpath = walk(childpath)
                    if childdirpath != '':
                        dir += f'{"  " * root.count("/")}- {child}\n'
                        dir += childdirpath

                if os.path.isfile(childpath) and not child.startswith('.') and not child.startswith('_') and (child.endswith('.md') or child.endswith('.markdown') ):
                    file += f'{"  " * root.count("/")}- [{child[:child.rfind(".")]}]({childpath.replace(" ", "%20")})\n'

            return f'{dir}{file}'

        with open('_sidebar.md', 'w') as f:
            f.write(walk('.'))

    def clean(self) -> None:
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.startswith('._'):
                    os.remove(os.path.join(dirpath, filename))

    def deploy(self) -> None:
        os.system('git add -A && git commit -m "`date`" && git push origin master')

if __name__ == '__main__':
    Deploy()
