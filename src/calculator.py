from constants import CONSTANTS


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


def calculateTimes(audiobookDetails):
    print('\n\n\n')
    print(audiobookDetails)
    totalTime = calculateTime(audiobookDetails[CONSTANTS.MP3_FILES], audiobookDetails[CONSTANTS.MP3_DURATIONS])
    elapsedTime = 0
    previousMp3Progress = 0
    if audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY] != None:
        previousMp3Progress = calculateTime(sublist_up_to(
            audiobookDetails[CONSTANTS.MP3_FILES], audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY]), audiobookDetails[CONSTANTS.MP3_DURATIONS])
        elapsedTime = previousMp3Progress + audiobookDetails[CONSTANTS.PROGRESS_SECOND_KEY]

    # percentage
    e = int(elapsedTime)
    t = int(totalTime)
    percentage = 0
    if t != 0:
        percentage = int((100*e)/t)

    return totalTime, elapsedTime, percentage
