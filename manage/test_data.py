def load_test_data(db):
    load_authors(db)
    load_sources(db)

def load_authors(db):
    authors = [ 
    { "name": "Elisha Livingston" },
    { "name": "Margret Mcbride" },
    { "name": "Nita Baxter" },
    { "name": "Sam Best" },
    { "name": "Theo Wolf" },
    { "name": "Brock Trujillo" },
    { "name": "Rosalie Boone" },
    { "name": "Mary Kennedy" },
    { "name": "Neal Dorsey" },
    { "name": "Shirley Powell" },
    { "name": "Jewell Obrien" },
    { "name": "Christie Woods" },
    { "name": "Johnnie Salas" },
    { "name": "Jessica Norris" },
    { "name": "Jarvis Ali" },
    { "name": "Milton Brewer" },
    { "name": "Sheryl Kent" },
    { "name": "Johnson Dudley" },
    { "name": "Erna Mcknight" },
    { "name": "Bernadine Randolph" },
    { "name": "Oswald P Grundersonn, MD" },
    { "name": "Editors" }
    ]
    db.executemany("INSERT INTO authors ( name ) "
                   " SELECT :name "
                   " WHERE NOT EXISTS ( SELECT 1 FROM authors WHERE name = :name );", authors)
    db.commit()

def load_sources(db):
    sources = [
        { "title": "Healthy Book", "author": "Elisha Livingston" },
        { "title": "Serious Journal", "author": "Margret Mcbride" },
        { "title": "Academic Journal", "author": "Editors" },
        { "title": "Popular Book", "author": "Oswald P Grundersonn, MD" },
        { "title": "Trendy Website", "author": "Johnson Dudley" },
        { "title": "News Website", "author": "Elisha Livingston" }
    ]
    db.executemany("INSERT INTO sources ( title, authorid ) "
                   " SELECT :title, id "
                   " FROM authors "
                   " WHERE name = :author "
                   " AND NOT EXISTS ( SELECT 1 FROM sources WHERE title = :title );" 
                   , sources)
    db.commit()