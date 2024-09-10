import requests

from bs4 import BeautifulSoup

from constants import RESET_TIME_ENDPOINT


def queryByPlayerName(playerName, season):
    try:
        r = requests.get(f'{RESET_TIME_ENDPOINT}', params={'q': playerName})
        r.raise_for_status()  # Kiểm tra nếu request thành công
        
        # Phân tích cú pháp HTML bằng BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Tìm bảng đầu tiên có class 'table-hover'
        table = soup.find('table', class_='table-hover')
        
        if table:
            # Tìm tất cả các hàng trong bảng
            rows = table.find_all('tr')
            
            for row in rows:
                # Tìm tất cả các cột trong hàng
                columns = row.find_all('td')
                
                # Nếu hàng này có ít nhất 2 cột (để kiểm tra cột 2 và cột cuối)
                if len(columns) >= 2:
                    # Lấy cột thứ hai
                    second_column = columns[1]
                    
                    # Tìm thẻ 'a' trong cột thứ hai
                    link = second_column.find('a')
                    
                    if link and link.has_attr('href'):
                        # Lấy href và phân tích thành các phần tử (phân cách bởi dấu '-')
                        href_parts = link['href'].split('-')
                        
                        # Kiểm tra nếu cụm đầu tiên trong đường dẫn khớp với season
                        if href_parts[0].endswith(season):
                            # Lấy cột cuối cùng
                            last_column = columns[-1]
                            
                            # Lấy `div` đầu tiên trong cột cuối cùng
                            first_div = last_column.find('div')
                            
                            if first_div:
                                # Lấy text từ `div` đầu tiên bên trong `first_div`
                                inner_div = first_div.find('div')
                                
                                if inner_div:
                                    # print(inner_div.text.strip())
                                    return inner_div.text.strip()
                                else:
                                    print("No inner div found")
        return False

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False


resetTime = queryByPlayerName('suarez', 'btb')
print(resetTime)