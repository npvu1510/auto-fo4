import datetime

def getTypeHour(hour):
    return 'chẵn' if hour % 2 == 0 else 'lẻ' 

def adjust_minute(minute, offset, is_start):
    if is_start:
        # Điều chỉnh startMinute lùi lại offset phút
        new_minute = (minute - offset) % 60
        # Kiểm tra nếu đã lùi về giờ trước
        return new_minute, new_minute > minute
    else:
        # Điều chỉnh endMinute tiến lên offset phút
        new_minute = (minute + offset) % 60
        # Kiểm tra nếu đã tiến lên giờ sau
        return new_minute, new_minute < minute


from copy import deepcopy
def isResetTime_v2(resetTime, offset=20):
    rst = deepcopy(resetTime)
    
    rst['startMinute'], isStartChanged = adjust_minute(rst['startMinute'], offset, True)
    rst['endMinute'], isEndChanged = adjust_minute(rst['endMinute'], offset, False)

    if isStartChanged:
        rst['startHourType'] = 'chẵn' if rst['startHourType'] == 'lẻ' else 'lẻ'
    if isEndChanged:
        rst['endHourType'] = 'chẵn' if rst['endHourType'] == 'lẻ' else 'lẻ'

    # Lấy thời gian hiện tại
    currentTime = datetime.datetime.now()
    current_hour = currentTime.hour
    current_minute = currentTime.minute

    # current_hour = 23
    # current_minute = 4

    # Kiểm tra khoảng thời gian
    message = ''
    # Trường hợp thông thường: rst['startMinute'] nhỏ hơn hoặc bằng rst['endMinute']
    # if rst['startMinute'] <= rst['endMinute']:
    if rst['startHourType'] == rst['endHourType']:
        if getTypeHour(current_hour) == rst['startHourType']:
            # Chưa tới giờ
            if current_minute < rst['startMinute']:
                message = message + f"{current_hour}:{rst['startMinute']}"

            # Đã qua giờ
            elif current_minute > rst['endMinute']:
                message = message + f"{(current_hour + 2) % 24}:{rst['startMinute']}"

            # Đang trong giờ
            else:
                return True
        else:
            message = message + f"{(current_hour + 1) % 24}:{rst['startMinute']}"

    # Trường hợp đặc biệt: rst['startMinute'] lớn hơn rst['endMinute'] (qua nửa đêm)
    else:
        if getTypeHour(current_hour) == rst['startHourType']:
            if current_minute < rst['startMinute']:
                message = message + f"{current_hour}:{rst['startMinute']}"
            else:
                return True

        if getTypeHour(current_hour) == rst['endHourType']:
            if current_minute > rst['endMinute']:
                message = message + f"{(current_hour + 1) % 24}:{rst['startMinute']}"
            else:
                return True

    return message



def time_until_reset(rst, offset=20):
    result = isResetTime_v2(rst, offset)

    if result is True:
        # return "Thời gian hiện tại đang nằm trong khoảng reset time."
        return True

    # result có định dạng "hh:mm"
    target_hour, target_minute = map(int, result.split(':'))

    # Lấy thời gian hiện tại
    currentTime = datetime.datetime.now()
    current_hour = currentTime.hour
    current_minute = currentTime.minute

    # Chuyển đổi thời gian hiện tại và thời gian đích thành số phút kể từ đầu ngày
    current_time_in_minutes = current_hour * 60 + current_minute
    target_time_in_minutes = target_hour * 60 + target_minute

    # Tính số phút còn lại
    if target_time_in_minutes >= current_time_in_minutes:
        minutes_until_reset = target_time_in_minutes - current_time_in_minutes
    else:
        # Nếu target time là ngày hôm sau
        minutes_until_reset = (24 * 60 - current_time_in_minutes) + target_time_in_minutes

    return f"{minutes_until_reset} phút nữa tới giờ reset."




def toResetTime(resetStr):
    split_parts = resetStr.split(' ')
    if len(split_parts) == 2:
        startMinute = int(split_parts[-1].split('-')[0])
        endMinute = int(split_parts[-1].split('-')[1])
        return {'startHourType': split_parts[0].lower(), 'startMinute':  startMinute, 'endHourType': split_parts[0].lower(),  'endMinute': endMinute}
    else:        
        return {'startHourType': split_parts[0].lower(), 'startMinute':  int(split_parts[1]), 'endHourType': split_parts[3].lower(),  'endMinute': int(split_parts[-1])}


