from bs4 import BeautifulSoup

OUT_FILE = 'top_Computer_Science_univs.csv'


# Parse university names from raw html
with open("Top_CS.html", "r") as f:
    soup = BeautifulSoup(f, 'html.parser')

univ_divs = soup.find_all("div", {"class": ["Box-w0dun1-0", "jSPhKa"]})


univ_names = []
for u in univ_divs:
    if 'name' in u.attrs:
        cur_u_name = u.attrs['name']
        univ_names.append(cur_u_name)


# Save data as csv
with open(OUT_FILE, "w") as f:
    header_line = 'id,name\n'
    f.write(header_line)

    for i in range(len(univ_names)):
        cur_u_id = i + 1
        cur_u_name = univ_names[i]
        data_line = f"{cur_u_id},'{cur_u_name}'\n"

        f.write(data_line)
