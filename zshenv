path+=('/Users/mmalchevskii/.local/bin')

alias up='bubu && mas upgrade && softwareupdate -i -a'

alias j=just
alias git-cleanup='git branch -vv | grep ': gone]' | grep -v '\*' | awk '{ print $1; }' | xargs -r git branch -d'

alias approve_olga='zkubectl login fulfillment && zkubectl cluster-access approve olsemernitsk'
alias approve_vadim='zkubectl login fulfillment && zkubectl cluster-access approve vturkov'

alias restart-podman='podman machine stop && podman machine start'
