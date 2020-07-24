import csv

def collect_citys():
     with open('city.csv', newline='', encoding='windows-1251') as f:
        fields = ['name']
        city_list = []
        reader = csv.DictReader(f, fields,delimiter=';')
        for row in reader:
            city_list.append(row[None][2])
        return(city_list)

if __name__ == '__main__':
    collect_citys()
