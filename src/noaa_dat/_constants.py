
BASE_URL = """https://services.dat.noaa.gov/arcgis/rest/services/nws_damageassessmenttoolkit/DamageViewer/MapServer/0/query?"""

"""{root_url}where={where}&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry={geometry}&geometryType=esriGeometryEnvelope&inSR=
&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields={out_fields}
&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR={out_sr}&havingClause=&returnIdsOnly=false
&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=
&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=
&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f={f}"""

WHERE = "where="
TEXT = "text="
OBJECT_IDS = "objectIds="
TIME= "time="
TIME_RELATION = "timeRelation="
GEOMETRY = "geometry="

OUT_FIELDS = """objectid%2Cstormdate%2Csurveydate%2Cevent_id%2Cdamage%2Cdamage_txt%2Cdod_txt%2Cefscale%2Cdamage_dir%2Cwindspeed%2Cinjuries%2Cdeaths%2Clat%2Clon%2Coffice%2Cgps_horiz_accuracy%2C%2Cglobalid%2Cedit_user%2Cedit_time%2Ccomments%2Cpath_guid"""
OUT_SR = "4326"

params = {
    "where":f"",
    "text":"",
    "objectIds":"",
    "time":"",
    "timeRelation":"esriTimeRelationOverlaps",
    "geometry":f"",
    "geometryType":"esriGeometryEnvelope",
    "inSR":"",
    "spatialRel":"esriSpatialRelIntersects",
    "distance":"",
    "units":"esriSRUnit_Foot",
    "relationParam":"",
    "outFields":f"",
    "returnGeometry":"true",
    "returnTrueCurves":"false",
    "maxAllowableOffset":"",
    "geomteryPrecision":"",
    "outSR":f"",
    "havingClause":"",
    "returnIdsOnly":"false",
    "returnCountOnly":"false",
    "orderByFields":"",
    "groupByFieldsForStatistics":"",
    "outStatistics":"",
    "returnZ":"false",
    "returnM":"false",
    "gdbVersion":"",
    "historicMoment":"",
    "returnDistinctValues":"false",
    "resultOffset":"",
    "resultRecordCount":"",
    "returnExtentOnly":"false",
    "sqlFormat":"none",
    "datumTransformation":"",
    "parameterValues":"",
    "rangeValues":"",
    "quantizationParameters":"",
    "featureEncoding":"esriDefault",
    "f":f""
}

