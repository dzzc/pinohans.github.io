## PS1

```bash
function parse_git_branch {
   git branch --no-color 2> /dev/null | sed -e "/^[^*]/d" -e "s/* \(.*\)/(\1)/"
}
export PS1="\[\e[1;35m\]\u\[\e[0m\]@\[\e[1;34m\]\h\[\e[0m\]:\[\e[1;32m\]\w\[\e[1;36m\] \$(parse_git_branch)\[\e[0m\]\$ "
```

