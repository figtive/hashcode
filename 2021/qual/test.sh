#!/bin/zsh

if [[ $1 = "killall" ]]; then
    ps -a | grep _temp | sed -e '$ d' | awk '{print $1}' | xargs kill -9
    exit
fi

TIMESTAMP=$(date +"%H%M%S")
EXEC="out/$TIMESTAMP/_temp-$TIMESTAMP.py"

mkdir -p "out/$TIMESTAMP"
cp $1 $EXEC
echo "======================================== $TIMESTAMP"
for FILENAME in $(find ./in -name '*.in' | sort); do
    CASE=${FILENAME:5:-3}
    python $EXEC $CASE < "in/$CASE.in" 2> "out/$TIMESTAMP/$CASE.out" &
done
wait
