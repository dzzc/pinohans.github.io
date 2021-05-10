## PS1

```bash
function parse_git_branch {
   git branch --no-color 2> /dev/null | sed -e "/^[^*]/d" -e "s/* \(.*\)/(\1)/"
}
autoload -U colors && colors
setopt PROMPT_SUBST
PROMPT='%B%F{magenta}%n%f%b@%B%F{blue}%m%f%b:%B%F{green}%1|%~%f %F{cyan}$(parse_git_branch)%f%b$ '
RPROMPT='[%B%F{yellow}%?%f%b]'
```

