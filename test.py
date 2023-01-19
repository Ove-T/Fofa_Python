import xlsxwriter

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
data = [1,2,3,4,5]
worksheet.write('A1', 'IP')
worksheet.write('B1', 'PORT')
worksheet.write('C1', 'protocol')
worksheet.write('D1', 'title')
worksheet.write('E1', 'domain')
worksheet.write_row('A2',data)
workbook.close()



