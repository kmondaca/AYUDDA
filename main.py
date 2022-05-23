from flask import Flask, render_template, session, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import (StringField , SubmitField,BooleanField ,
                     RadioField , SelectField , TextField , TextAreaField)

from wtforms.validators import DataRequired
from util import fill_one_pdf
import os

app = Flask(__name__) #create application

app.config['SECRET_KEY'] = 'mykey'

class InfoForm(FlaskForm):
    first = StringField('First Name: ', validators=[DataRequired()])
    last = StringField('Last Name: ', validators=[DataRequired()])
    lang = StringField('Primary Language:')
    phone = StringField('phone', validators=[DataRequired()])
    conpref =  RadioField('Contact Preference:',
                      choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    email = TextAreaField('')
    conchoice =TextAreaField('')
    submit = SubmitField('Submit')


##############################

class SpanForm(FlaskForm):
    sfirst = StringField('Primer nombre: ', validators=[DataRequired()])
    slast = StringField('Apellido: ', validators=[DataRequired()])
    slang = StringField('Idioma principal:')
    sphone = StringField('Teléfono:', validators=[DataRequired()])
    sconpref =  RadioField('Cómo prefiere comunicarse:',
                      choices=[('phone', 'Teléfono'), ('email', 'Correo electrónico'), ('both', 'Ambos')])
    sconchoice =TextAreaField('')
    semail = TextAreaField('')
    submit = SubmitField('Submit')

class TestForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    dob = StringField("Date of Birth: ", validators=[DataRequired()])
    submit = SubmitField('Submit')

#will continue to have this coded in English, need to fix discriptions to Spanish
class SectionA(FlaskForm):
    childName = StringField('Nombre completo: ', validators=[DataRequired()])
    childDOB = StringField("Fecha de nacimiento: ", validators=[DataRequired()])
    childSex = RadioField('Sexo:',
                      choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    AHCCCS =StringField('Numero de cuenta de AHCCCS (Si corresponde):')
    language = StringField('Idioma principal:', validators=[DataRequired()])
    childAddress = StringField('Direccion residencial (Numero, Calle):', validators=[DataRequired()])
    childCity = StringField('Ciudad:', validators=[DataRequired()])
    childState = StringField('Estado:', validators=[DataRequired()])
    childZip = StringField('Codigo postal:', validators=[DataRequired()])
    phone = StringField('Teléfono:', validators=[DataRequired()])
    ethnicity = RadioField('Etnia:',
                         choices=[('Indígena de los EE UU/Alaska', 'Indígena de los EE UU/Alaska'),
                                  ('Negra/Afroamericana (no Hispánica)', 'Negra/Afroamericana (no Hispánica)') ,
                                  ('Asiática/Indígena de la Polinesia', 'Asiática/Indígena de la Polinesia'),
                                  ('Hispánica o Latina', 'Hispánica o Latina'),
                                  ('Otra'), ('Otra'),
                                  ('Blanca (no Hispánica)', 'Blanca (no Hispánica)')])


    tribe = StringField('Tribu (Si corresponde):')
    childMailAddress = StringField('Dirección postal (Si corresponde):', validators=[DataRequired()])
    childMailCity = StringField('Ciudad:', validators=[DataRequired()])
    childMailState = StringField('Estado:', validators=[DataRequired()])
    childMailZip = StringField('Código postal:', validators=[DataRequired()])
    conpref = RadioField('Cómo prefiere comunicarse::',
                         choices=[('Teléfono', 'Teléfono'), ('Correo electrónico', 'Correo electrónico'), ('Ambos', 'Ambos')])
    email = TextAreaField('')
    vote = RadioField('¿Desea registrarse para votar?',
                         choices=[('Sí', 'Sí'), ('No', 'No')])
    submit = SubmitField('Enviar')


class SectionA1(FlaskForm):
    profName = StringField('Nombre de contacto', validators=[DataRequired()])
    profPhone = StringField('Teléfono de contacto', validators=[DataRequired()])
    type = StringField('Tipo de profesional', validators=[DataRequired()])
    date = StringField('Fecha de evaluación', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionB(FlaskForm):
    parentName = StringField('Nombre completo:', validators=[DataRequired()])
    relationship = StringField("Parentesco:", validators=[DataRequired()])
    parentPhone = StringField('Teléfono:', validators=[DataRequired()])
    parentEmail = TextAreaField('')
    parentAddress = StringField('Dirección (si diferente al solicitante):', validators=[DataRequired()])
    parentCity = StringField('Ciudad:', validators=[DataRequired()])
    parentState = StringField('Estado:', validators=[DataRequired()])
    parentZip = StringField('Código postal:', validators=[DataRequired()])
    parentConpref = RadioField('Mejor manera de contactarlo:',
                         choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    legalName = StringField('Nombre del tutor legal (Si diferente al anterior):', validators=[DataRequired()])
    legalRelationship = StringField("Parentesco:", validators=[DataRequired()])
    legalPhone = StringField('Teléfono:', validators=[DataRequired()])
    legalAddress = StringField('Dirección:', validators=[DataRequired()])
    legalCity = StringField('Ciudad:', validators=[DataRequired()])
    legalState = StringField('Estado:', validators=[DataRequired()])
    legalZip = StringField('Código postal:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionC(FlaskForm):
    coverage = StringField('Type of Coverage:', validators=[DataRequired()])
    healthPlan = StringField('Name of Health Plan:', validators=[DataRequired()])
    policyName = StringField('Policy Holder Name:', validators=[DataRequired()])
    IDNum = StringField('ID/Group Number:', validators=[DataRequired()])
    policyNum = StringField('Policy Number:', validators=[DataRequired()])
    policyDate = StringField('Effective Date:', validators=[DataRequired()])
    dob = StringField("Policy Holder's Date of Birth:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionD(FlaskForm):
    program = StringField('Early Intervention Program or School Name and School District:', validators=[DataRequired()])
    typeSupport = StringField('Type of Support(IEP or 504 plan)', validators=[DataRequired()])
    eduDate = StringField('Dates Attended:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionHIPAA(FlaskForm):
    #concat name ,last, first middle (cannot get previous since middle isn't specified
    childLast = StringField("Child's first name:", validators=[DataRequired()])
    childFirst = StringField("Child's last name:", validators=[DataRequired()])
    childMiddle = StringField("Child's middle name:", validators=[DataRequired()])
    #DOB request, gather from Section A
    describeInfo = TextAreaField('')
    agency = StringField("Agency requesting information:", validators=[DataRequired()])
    requestDate= StringField("Date of Request:", validators=[DataRequired()])
    #get Parent name
    #need a physical signature....
    authorizationDate = StringField("Date of Authorization:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionRelease(FlaskForm):
    #get concat version from SectionHIPAA of name
    #get dob from SectionA
    #get agency
    #get request date
    office = RadioField('Which Division of Deveopmental Disabilities office is closest?:',
                               choices=[('Chandler', 'Chandler'),
                                        ('Flagstaff', 'Flagstaff'),
                                        ('Tucson', 'Tucson'),
                                        ('Phoenix (West)', 'Phoenix (West)'),
                                        ('Phoenix (Central)', 'Phoenix (Central)')])
    #autofill the location of the office
    permissions = SelectField("Permito que la informacion de salud protegida marcada a continuacion se comparta con el profesionalmedico, la agencia, el entorno educativo u otro indicado anteriormente::",
                               choices=[('Expedientes medicos', 'Expedientes medicos'),
                                        ('Informes/Expedientes de audiologia', 'Informes/Expedientes de audiologia'),
                                        ('Informes del habla y lenguaje', 'Informes del habla y lenguaje'),
                                        ('Informe de Plan 504 o Plan de Educacion Individual y Evaluacion mas reciente', 'Informe de Plan 504 o Plan de Educacion Individual y Evaluacion mas reciente'),
                                        ('Registros de recien nacidos', 'Registros de recien nacidos'),
                                        ('Informes psicologicos', 'Informes psicologicos'),
                                        ('Informes de terapia fisica', 'Informes de terapia fisica'),
                                        ('Registros de nacimiento y parto', 'Registros de nacimiento y parto'),
                                        ('Informes de terapia ocupacional', 'Informes de terapia ocupacional'),
                                        ('Expedientes de salud conductual', 'Expedientes de salud conductual'),
                                        ('Otro (Especifique):', 'Otro (Especifique):')])
    other = StringField("")
    #get parent name
    #requires real signature
    #get date of authorization
    submit = SubmitField('Enviar')
####################################################################
# This is 90% of the magic right here (see https://pypi.org/project/fillpdf/):
from fillpdf.fillpdfs import (
    get_form_fields,
    write_fillable_pdf,
)

# constants for filenames
BLANK_FORM = "DDD-2069A-S-blank.pdf"
COMPLETED_FORM = "DDD-2069A-S-completed.pdf"

#pdf is in directory it knows what to get
form_fields = get_form_fields(BLANK_FORM)

# Just to see how everything starts out
for childName, current_value in form_fields.items():
    if current_value == "":
        current_value = "<blank>"
    print(f"{childName}: {current_value}")

# Prep data to fill out a few entries
updates = dict(
    SecA_Name="gfhgfd" ,
    Sex="Female",
    HomeAdd="La Casita",
    A_City1="Cartagena, Colombia",
    A1_name1="Abuela Alma",
    A1_Type1="Matriarch",
    A1_Date1="11/24/2021"
)

# Produce a non-editable version with entries filled in
write_fillable_pdf(BLANK_FORM, COMPLETED_FORM, updates, flatten=True)

# MAC ONLY
os.system(f"open {COMPLETED_FORM}")


####################################################################

@app.route('/english', methods=['GET', 'POST'])
def english():

    form = InfoForm()
    if form.validate_on_submit():
        session['first']= form.first.data
        session['last'] = form.last.data
        session['lang'] = form.lang.data
        session['phone'] = form.phone.data
        session['conpref'] = form.conpref.data
        session['conchoice'] = form.conchoice.data
        session['email'] = form.email.data
        #session['submit'] = form.submit.data

        return redirect(url_for("thankyou"))#only when form submitted

    return render_template('english.html',form=form) #app

@app.route('/spanish', methods=['GET', 'POST'])
def spanish():
    form = SpanForm()
    if form.validate_on_submit():
        session['sfirst'] = form.sfirst.data
        session['slast'] = form.slast.data
        session['slang'] = form.slang.data
        session['sphone'] = form.sphone.data
        session['sconpref'] = form.sconpref.data
        session['sconchoice'] = form.sconchoice.data
        session['semail'] = form.semail.data
        # session['submit'] = form.submit.data

        return redirect(url_for("gracias"))  # only when form submitted

    return render_template('spanish.html', form=form)  # app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/einfo')
def einfo():
    return render_template('einfo.html')

@app.route('/sinfo')
def sinfo():
    return render_template('sinfo.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    # for the other classes, I can just so SectionB.variable.data to grab the info
    form = SectionA()
    if form.validate_on_submit():
        print("HERE")
        data_for_pdf = dict(
            SecA_Name=form.Childname.data,
            appDOB=form.childDOB.data,
            Sex=form.childSex.data,
            HomeAdd=form.childAddress.data,
            A_City1=form.childCity.data,
            A_State1=form.childState.data,
            A_Zip=form.childZip.data,
            A_Phone=form.phone.data,
            A_ethnicity=form.ethnicity.data,
            A_tribe=form.tribe.data,
            A_mailAdd=form.childMailAddress.data,
            A_MailCity=form.childMailCity.data,
            A_MailState=form.childMailState.data,
            A_MailZip=form.childMailZip.data,
            A_conpref = form.conpref.data,
            A_email = form.email.data,
            A_conchoice = form.conchoice.data,
            A_vote = form.vote.data,
            A1_name1="Abuela Alma",
            A1_Type1="Matriarch",
            A1_Date1="11/24/2021"
        )
        complete_pdf = fill_one_pdf("DDD-2069A-S", data_for_pdf)
        return send_file(complete_pdf, as_attachment=True)
    else:
        return render_template('test.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)
