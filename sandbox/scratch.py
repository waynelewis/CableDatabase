		
page = markup.page( )
page.init( title="NSLSII Beamlines Cable Database",
           css = 'cdb.css')
page.div.open(align = "center")
page.img(src = "bnl_logo.png", width = "300px")
page.h1("TEST")
page.div.close()
page.div.open(align = "center")
page.table.open( class_ = 'gridtable' )
page.tbody.open()

for row in rows:
    page.tr.open()
    page.td()
    for item in row[4:]:
        page.td(item)
    page.tr.close()
page.tbody.close()
page.table.close()
page.div.close()

print "Content-type: text/html\n\n";
print page
