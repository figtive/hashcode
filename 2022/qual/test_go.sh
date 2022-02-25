#!/bin/zsh

if [[ $1 = "killall" ]]; then
    ps -a | grep _temp | sed -e '$ d' | awk '{print $1}' | xargs kill -9
    exit
fi

TIMESTAMP=$(date +"%H%M%S")
TEMP="out/$TIMESTAMP/temp-$TIMESTAMP.go"
TEMP_EXEC="out/$TIMESTAMP/solver"

mkdir -p "out/$TIMESTAMP"
cp $1 $TEMP

go build -o $TEMP_EXEC $TEMP

echo "======================================== $TIMESTAMP"
for FILENAME in $(find ./in -name '*.in' | sort); do
    CASE=${FILENAME:5:-3}
    $TEMP_EXEC $CASE < "in/$CASE.in" > "out/$TIMESTAMP/$CASE.out" &
done
wait
