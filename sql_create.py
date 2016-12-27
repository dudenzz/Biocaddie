import sqlite3

conn = sqlite3.connect('biocaddie.db')

with conn:
    cur = conn.cursor()
    #cur.execute("drop table common")
    cur.execute(
        "CREATE TABLE common(id integer primary key, filename text, title text, repository text)")
    cur.execute(
        "create table arrayexpress(id integer, title text, description text, species text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table cia(id integer, anatomicalPartname text, diseasename text, organismname text, organismscientificname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table bioproject(id integer, organismtargetspecies text, organismtargetstrain text, dataItemkeywords text, dataItemdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table clinicaltrials(id integer, gender text, criteria text, phase text, city text, country text, othercountries text, studyType text, StudyGrouptype text, StudyGroupdescription text, StudyGroupname text, Diseasename text, Treatmentdescription text, Treatmentagent text, Treatmenttitle text, keyword text, Datasetdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table ctn(id integer, organismscientificName text, organismname text, datasetdescription text, datasetkeywords text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table cvrg(id integer, datasetdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table dataverse(id integer, publicationdescription text, datasetdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table dryad(id integer, datasetdescription text, datasetkeywords text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table gemma(id integer, organismcommonName text, dataItemtitle text, dataItemdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table geo(id integer, dataItemtitle text, dataItemsource_name text, dataItemorganism text, dataItemdescription text, htmldata text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table mpd(id integer, datasettitle text, datasetdescription text, datasetdataType text, datasetgender text, organismstrain text, organismscientificName text, organismname text, dimensionname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table neuromorpho(id integer, studyGroupname text, anatomicalPartname text, datasetnote text, cellname text, treatmenttitle text, organismstrain text, organismscientificName text, organismname text, organismgender text, dimensionname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table nursadatasets(id integer, dataAcquisitiontitle text, publicationdescription text, datasetkeywords text, datasetdescription text, datasettitle text, organismname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table openfmri(id integer, dataAcquisitiontitle text, datasettitle text, datasetdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table peptideatlas(id integer, datasettitle text, datasetdescription text, instrumentname text, treatmentdescription text, organismstrain text, organismname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table phenodisco(id integer, MESHterm text, title text, inexclude text, desc text, gender text, disease text, history text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table physiobank(id integer, datasettitle text, datasetdataType text, datasetdescription text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table proteomexchange(id integer, instrumentname text, datasettitle text, keywords text, organismname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table yped(id integer, dataAcquisitiontitle text, datasetdescription text, datasettitle text, organismname text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table pdb(id integer, dataItemtitle text,dataItemdescription text,dataItemkeywords text,organismsourcescientificName text,organismhostscientificName text,genename text, FOREIGN KEY(id) REFERENCES common(id))")
    cur.execute(
        "create table fillscore(id integer, score real, FOREIGN KEY(id) REFERENCES common(id))")