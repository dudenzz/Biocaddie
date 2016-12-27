import sqlite3

conn = sqlite3.connect('biocaddie.db')

with conn:
    cur = conn.cursor()

    cur.execute("drop table arrayexpress")
    cur.execute("drop table cia")
    cur.execute("drop table bioproject")
    cur.execute("drop table clinicaltrials")
    cur.execute("drop table ctn")
    cur.execute("drop table cvrg")
    cur.execute("drop table dataverse")
    cur.execute("drop table dryad")
    cur.execute("drop table gemma")
    cur.execute("drop table geo")
    cur.execute("drop table mpd")
    cur.execute("drop table neuromorpho")
    cur.execute("drop table nursadatasets")
    cur.execute("drop table openfmri")
    cur.execute("drop table peptideatlas")
    cur.execute("drop table phenodisco")
    cur.execute("drop table physiobank")
    cur.execute("drop table proteomexchange")
    cur.execute("drop table yped")
    cur.execute("drop table common")
    cur.execute("drop table pdb")
    cur.execute("drop table fillscore")
