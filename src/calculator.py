
def sublist_up_to(lst, element):
    try:
        index = lst.index(element)
        return lst[:index]
    except ValueError:
        return []


def calculateTime(mp3Files, mp3Lengths):
    time = 0
    for s in mp3Files:
        time += int(mp3Lengths[s])
    return time


def calculateTimes(mp3Name, mp3Seconds, mp3Files, mp3Lengths):
    totalTime = calculateTime(mp3Files, mp3Lengths)
    elapsedTime = 0
    previousMp3Progress = 0
    currentMp3Progress = 0
    if mp3Name != None:
        previousMp3Progress = calculateTime(sublist_up_to(
            mp3Files, mp3Name), mp3Lengths)
        currentMp3Progress += mp3Seconds
        elapsedTime = previousMp3Progress + currentMp3Progress

    # percentage
    e = int(elapsedTime)
    t = int(totalTime)
    percentage = 0
    if t != 0:
        percentage = int((100*e)/t)

    return totalTime, elapsedTime, previousMp3Progress, currentMp3Progress, percentage
