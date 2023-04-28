 #!/bin/bash
konsole --geometry 600x400+0+0 -e /bin/bash -c "ls -la; $SHELL" \
& konsole --geometry 600x400+620+0 -e /bin/bash -c "ls; $SHELL" \

