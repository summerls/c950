class clock:

    def __init__(self):
        self.hour = 8
        self.minutes = 0
        self.seconds = 0

    def elapseTime(self, hours):
        hoursInt = int(hours/1)
        hoursRemainder = (hours % 1)
        minutes = hoursRemainder*60
        minutesInt = int(hoursRemainder*60)

        seconds = (minutes % 1) * 60
        self.elapseMinutes(minutesInt)
        self.elapseHours(hoursInt)
        self.elapseSeconds(seconds)

    def elapseMinutes(self, minutes):
        self.minutes +=minutes
        if self.minutes > 60:
            hours = int(self.minutes / 60)
            remainingMinutesInt = int(self.minutes % 60)
            seconds = ((self.minutes % 60) - remainingMinutesInt) * 60
            self.hour += hours
            self.minutes = remainingMinutesInt
            self.elapseSeconds(seconds)
        remainderMinutes = self.minutes % 1
        if remainderMinutes != 0:
            self.elapseSeconds(remainderMinutes*60)

    def elapseSeconds(self, seconds):
        self.seconds +=seconds
        if self.seconds > 60:
            excessSeconds = int(self.seconds / 60)
            remainingSeconds = self.seconds % 60
            self.elapseMinutes(excessSeconds)
            self.seconds = remainingSeconds

    def elapseHours(self, hours):
        self.hour+=hours

    def getTime(self):
        time = str(self.hour) + ":" + str(self.minutes) + ":" + str(self.seconds)
        return time

    def getHour(self):
        return self.hour

    def getMinute(self):
        return self.minutes