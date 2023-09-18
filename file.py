def save_file(file_name, jobs):
  file = open(f"{file_name}.csv", "w")
  # write the header of file
  file.write('Title,Company,Location,URL\n')

  print(f'[file.py] total {len(jobs)} jobs are found.')
  for job in jobs:
    file.write(
      f"{job['title']},{job['company']},{job['region']},{job['link']}\n")

  file.close()