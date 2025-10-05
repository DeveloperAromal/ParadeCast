from datetime import datetime

def generate_historic_dates(current_date, total_years_back):
    
    
    dates = []
    
    date_obj = datetime.strptime(current_date, "%Y%m%d")
    
    
    
    for i in range(1, total_years_back + 1):
        
        past_year = date_obj.year - i
        
        
        try:
            historic_dates = date_obj.replace(year=past_year).strftime("%Y%m%d")
            dates.append(historic_dates)
            
        except ValueError as e:
            
            dates.append(date_obj.replace(year=past_year, day=28).strftime("%Y%m%d"))
            
        
    return dates
        
        
    
    
    
current = "20251005"
historic_dates = generate_historic_dates(current, total_years_back=10)
print(historic_dates)
    
    
    
    
    