clear

# Load .bashrc
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

if [ "$(tty)" = "/dev/tty1" ] && [ -z "$SCRIPT_RUNNING" ]; then
    export SCRIPT_RUNNING=1
    exec script -q -f ~/.tty1.log
fi

case "$(tty)" in
    /dev/tty2)
        python3 ~/splash.py "claude-chat" "starting..."
        python3 ~/claude-chat.py
        ;;
    /dev/tty3)
        python3 ~/splash.py "journal" "starting..."
        python3 ~/journal.py
        ;;
esac
