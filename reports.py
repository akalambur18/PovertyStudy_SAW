from jinja2 import Environment, FileSystemLoader
import pdfkit
import os


# We can specify any directory for the loader but for this example, use current directory
def report(dateTime, Validation_1, Validation_2, files):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("myreport.html")
    if(len(files)>0):
        files =  files.to_html(index=False)
    else:
        files = "No errors"
    if(len(Validation_1)>0):
        Validation_1_result =  Validation_1.to_html(index=False)
    else:
        Validation_1_result = "No errors"

    if(len(Validation_2)>0):
        Validation_2_result =  Validation_2.to_html(index=False)
    else:
        Validation_2_result = "No errors"

    template_vars = {"title" : "Summary Report",
                     "files" : files,
                    "Summary_V1" : "Total error during Validation 1 =  " +str(len(Validation_1)),
                    "Errors_in_Validation_1": Validation_1_result,
                    "Summary_V2" : "Total error during Validation 2 =  " +str(len(Validation_2)),
                    "Errors_in_Validation_2":Validation_2_result}

    # Create html and the PDF using our css style file
    html_out = template.render(template_vars)
    fileName = "Report_" + str(dateTime)
    completeName = os.path.join("Reports/", fileName + ".pdf")

    pdfkit.from_string(html_out, completeName)