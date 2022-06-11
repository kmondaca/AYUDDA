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
class SectionBForm(FlaskForm):
    parentName = StringField('Nombre completo:', validators=[DataRequired()])
    relationship = StringField("Parentesco:", validators=[DataRequired()])
    parentPhone = StringField('Teléfono:', validators=[DataRequired()])
    parentEmail = StringField('Correo electrónico:')
    parentAddress = StringField('Dirección:')
    parentCity = StringField('Ciudad:')
    parentState = StringField('Estado:')
    parentZip = StringField('Código postal:')
    vive = RadioField('¿Vive el solicitante con usted?:',
               choices=[('Yes', 'Sí'), ('No', 'No')])
    parentConpref = RadioField('Mejor manera de contactarlo:',
                         choices=[('Telefono', 'Telefono'), ('email', 'Correo Electronico'), ('Ambos', 'Ambos')])
    legalName = StringField('Nombre del tutor legal (Si diferente al anterior):')
    legalRelationship = StringField("Parentesco:")
    legalPhone = StringField('Teléfono:')
    legalAddress = StringField('Dirección:')
    legalCity = StringField('Ciudad:')
    legalState = StringField('Estado:')
    legalZip = StringField('Código postal:')
    submit = SubmitField('Enviar')

class SectionAForm(FlaskForm):
    childName = StringField('Nombre completo: ', validators=[DataRequired()])
    childDOB = StringField("Fecha de nacimiento: ", validators=[DataRequired()])
    childSex = RadioField('Sexo:',
                      choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    AHCCCS =StringField('Numero de cuenta de AHCCCS (Si corresponde):')
    language = StringField('Idioma principal:', validators=[DataRequired()])
    childAddress = StringField('Direccion residencial (Numero, Calle):')
    childCity = StringField('Ciudad:')
    childState = StringField('Estado:')
    childZip = StringField('Codigo postal:')
    childPhone = StringField('Telefono:', validators=[DataRequired()])
    ethnicity = RadioField('Etnia:',
                         choices=[('Indígena de los EE UU/Alaska', 'Indígena de los EE UU/Alaska'),
                                  ('Negra/Afroamericana (no Hispánica)', 'Negra/Afroamericana (no Hispánica)') ,
                                  ('Asiática/Indígena de la Polinesia', 'Asiática/Indígena de la Polinesia'),
                                  ('Hispánica o Latina', 'Hispánica o Latina'),
                                  ('Otra', 'Otra'),
                                  ('Blanca (no Hispánica)', 'Blanca (no Hispánica)')])
    tribe = StringField('Tribu (Si corresponde):')
    childMailAddress = StringField('Dirección postal (Si corresponde):')
    childMailCity = StringField('Ciudad:')
    childMailState = StringField('Estado:')
    childMailZip = StringField('Código postal:')
    childConpref = RadioField('Cómo prefiere comunicarse:',
                         choices=['Teléfono', 'Correo electrónico', 'Ambos'])
    childEmail = StringField('Correo electrónico de usted:')
    vote = RadioField('¿Desea registrarse para votar?',
                         choices=[('Sí', 'Sí'), ('No', 'No')])
    submit = SubmitField('Enviar')


class SectionA1Form(FlaskForm):
    profName = StringField('Nombre de contacto', validators=[DataRequired()])
    profPhone = StringField('Teléfono de contacto', validators=[DataRequired()])
    type = StringField('Tipo de profesional', validators=[DataRequired()])
    date = StringField('Fecha de evaluación', validators=[DataRequired()])
    submit = SubmitField('Enviar')



class SectionCForm(FlaskForm):
    coverage = StringField('Tipo de cobertura(privada,pública, etc.):', validators=[DataRequired()])
    healthPlan = StringField('Nombre del plan de salud:', validators=[DataRequired()])
    policyName = StringField('Nombre del titular de la póliza:', validators=[DataRequired()])
    IDNum = StringField('Número de ID/Grupo:', validators=[DataRequired()])
    policyNum = StringField('Número de póliza:', validators=[DataRequired()])
    policyDate = StringField('Fecha de vigencia:', validators=[DataRequired()])
    dob = StringField("Fecha de nacimiento del titular:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionDForm(FlaskForm):
    program = StringField('Estado del Programa de Intervención Temprana o Nombre de la escuela y del distrito escolar:', validators=[DataRequired()])
    typeSupport = StringField('Tipo de Apoyo (Servicios o tipo de plan tal cómo Plande Educación Individual o Plan 504):', validators=[DataRequired()])
    eduDate = StringField('Fechas que asistió:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionHIPAAForm(FlaskForm):
    #concat name ,last, first middle (cannot get previous since middle isn't specified
    childLast = StringField("Nombre de persona/cliente cuya información de la salud se compartirá:", validators=[DataRequired()])
    childFirst = StringField("Apellido de persona/cliente cuya información de la salud se compartirá::", validators=[DataRequired()])
    childMiddle = StringField("Segundo de persona/cliente cuya información de la salud se compartirá::", validators=[DataRequired()])
    #DOB request, gather from Section A
    describeInfo = TextAreaField('')
    agency = StringField("Persona/Agencia que solicita o necesita la información:", validators=[DataRequired()])
    requestDate= StringField("Fecha de solicitud:", validators=[DataRequired()])
    #get Parent name
    #need a physical signature....
    authorizationDate = StringField("Fecha de autorización:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionReleaseForm(FlaskForm):
    #get concat version from SectionHIPAA of name
    #get dob from SectionA
    #get agency
    #get request date
    office = RadioField('¿Qué oficina de la División de Discapacidades del Desarrollo es la más cercana?:',
                               choices=[('Chandler', 'Chandler'),
                                        ('Flagstaff', 'Flagstaff'),
                                        ('Tucson', 'Tucson'),
                                        ('Phoenix (Oeste)', 'Phoenix (Oeste)'),
                                        ('Phoenix (Central)', 'Phoenix (Central)')])
    #autofill the location of the office
    InfoTipo1 = RadioField('Expedientes medicos',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo2 = RadioField('Informes/Expedientes de audiologia',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo3 = RadioField('Informes del habla y lenguaje',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo4 = RadioField('Informe de Plan 504 o Plan de Educacion Individual y Evaluacion mas reciente',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo5 = RadioField('Registros de recien nacidos',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo6 = RadioField('Informes psicologicos',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo7 = RadioField('Informes de terapia fisica',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo8 = RadioField('Registros de nacimiento y parto',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo9 = RadioField('Informes de terapia ocupacional',
                           choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo10 = RadioField('Expedientes de salud conductual',
                            choices=[('On', 'Sí'), ('Off', 'No')])
    InfoTipo11 = RadioField('Informes/Expedientes de audiologia',
                            choices=[('On', 'Sí'), ('Off', 'No')])
    other = StringField("")
    #get parent name
    #requires real signature
    #get date of authorization
    submit = SubmitField('Enviar')
####################################################################
""""
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
    secA_AppName = "Doctor Strange",
    InfoTipo1 = "On",
    InfoTipo2 = "Off",
    InfoTipo3 = "On",
    InfoTipo4 = "Off"
    #secA_Contact="Correo electrónico"
    #secA_ContactPrefer= "lionel@email.com",
    #secA_Vote = "Sí",

    
)

# Produce a non-editable version with entries filled in
write_fillable_pdf(BLANK_FORM, COMPLETED_FORM, updates, flatten=True)

# MAC ONLY
os.system(f"open {COMPLETED_FORM}")

"""
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/falso')
def falso():
    return render_template('fake.html')

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

@app.route('/app', methods=['GET', 'POST'])
def sectionB():
    #Section B
    #Section A
    #Section C
    #Section D
    #Section A.1
    #HIPAA
    #Release

    #maybe nested ifs until the end.....otherwise just move it to the respective rendering
    #issues figuring out how to run it.....
    form = SectionBForm()
    if form.validate_on_submit():
        session['secB_Name'] = form.parentName.data
        session['secB_Relationship1'] = form.relationship.data
        session['secB_Phone1'] = form.parentPhone.data
        session['secB_Email1'] = form.parentEmail.data
        session['secB_Address1'] = form.parentAddress.data
        session['secB_City1'] = form.parentCity.data
        session['secB_State1'] = form.parentState.data
        session['secB_Zip1'] = form.parentZip.data
        session['viva'] = form.vive.data
        session['secB_BestWay'] = form.parentConpref.data
        session['secB_LGName'] = form.legalName.data
        session['secB_Relationship2'] = form.legalRelationship.data
        session['secB_Phone2'] = form.legalPhone.data
        session['secB_Address2'] = form.legalAddress.data
        session['secB_City2'] = form.legalCity.data
        session['secB_State2'] = form.legalState.data
        session['secB_Zip2'] = form.legalZip.data

        #just for the pdf to not complain
        session['secB_Alt'] = ""
        #it is not reading this redirect, I have tried changing it to another to see if it
        #would read it but no luck, really don't know what to do
        return redirect(url_for("sectionA"))  # only when form submitted


    return render_template('SectionB.html', form=form)  #this form refers to the form we set on 371

@app.route('/sectionA',methods=['GET', 'POST'])
def sectionA():
    form = SectionAForm()
    if form.validate_on_submit():
        session['secA_AppName'] = form.childName.data
        session['APPLICANT_DOB'] = form.childDOB.data
        session['APPLICANT_Sex'] = form.childSex.data
        session['secA_AHCCCS'] = form.AHCCCS.data
        session['secA_Language'] = form.language.data
        session['secA_HomeAddress'] = form.childAddress.data
        session['secA_City1'] = form.childCity.data
        session['secA_State1'] = form.childState.data
        session['secA_Zip1'] = form.childZip.data
        #let's make sure we are still holding onto the data we get from the child
        #regardless if they live at home or not

        if session['viva'] != 'Yes':
            session['secA_HomeAddress'] = form.childAddress.data
            session['secA_City1'] = form.childCity.data
            session['secA_State1'] = form.childState.data
            session['secA_Zip1'] = form.childZip.data
        else:
            session['secA_HomeAddress'] = session['secB_Address1']
            session['secA_City1'] = session['secB_City1']
            session['secA_State1'] = session['secB_State1']
            session['secA_Zip1'] = session['secB_Zip1']

        session['SecA_Phone'] = form.childPhone.data
        session['secA_Ethnicity'] = form.ethnicity.data
        session['secA_Tribe'] = form.tribe.data
        session['secA_MailingAdd'] = form.childMailAddress.data
        session['secA_City2'] = form.childMailCity.data
        session['secA_State2'] = form.childMailState.data
        session['secA_Zip2'] = form.childMailZip.data
        #switching contactprefer and contact to see if that resolves issue
        session['secA_ContactPrefer'] =form.childEmail.data
        session['secA_Contact'] =  form.childConpref.data
        session['secA_Vote'] = form.vote.data
        return redirect(url_for("sectionC"))  # only when form submitted

    return render_template('SectionA.html', form=form)


@app.route('/sectionC',methods=['GET', 'POST'])
def sectionC():
    form = SectionCForm()
    if form.validate_on_submit():
        session['secC_tipo1'] = form.coverage.data
        session['secC_plan1'] = form.healthPlan.data
        session['secC_Titular1'] = form.policyName.data
        session['secC_num1'] = form.IDNum.data
        session['secC_vigencia1'] = form.dob.data
        session['secC_naci1'] = form.policyDate.data
        #'secC_tipo2','secC_plan2','secC_Titular2','secC_num2','secC_vigencia2','secC_naci2',

        #just so the pdf filler doesn't complain
        session['secC_tipo2'] = ""
        session['secC_plan2'] = ""
        session['secC_Titular2'] = ""
        session['secC_num2'] = ""
        session['secC_vigencia2'] = ""
        session['secC_naci2'] = ""
        return redirect(url_for("sectionD"))  # only when form submitted

    return render_template('SectionC.html', form = form)

@app.route('/sectionD',methods=['GET', 'POST'])
def sectionD():
    form = SectionDForm()
    if form.validate_on_submit():
        session['secD_estado1'] = form.program.data
        session['secD_tipo1'] = form.typeSupport.data
        session['secD_fechas1'] = form.eduDate.data
        #unsure if I can assign the other values we already have here
        session['SIG_Name'] = session['secB_Name']
        session['SIG_Relationship']=session['secB_Relationship1']
        session['SIG_Date'] = session['3_Date1']
        #'secD_estado2','secD_tipo2', 'secD_fechas2',','SIG_Relationship','SIG_Date',

        #just so the pdf doesn't complain
        session['secD_estado2'] = ""
        session['secD_tipo2'] = ""
        session['secD_fechas2'] = ""

        return redirect(url_for("sectionA1"))  # only when form submitted

    return render_template('SectionD.html', form=form)


@app.route('/sectionA1',methods=['GET', 'POST'])
def sectionA1():
    form = SectionA1Form()
    if form.validate_on_submit():
        session['SecA_nombre1'] = form.profName.data
        session['SecA_Tipo1'] = form.type.data
        session['SecA_fecha1'] = form.date.data
        #'SecA_nombre2','Sec_Tipo2','SecA_fecha2','SecA_nombre3','SecA_Tipo3','SecA_fecha3',

        #adding to satisfy the pdf
        session['SecA_nombre2'] = ""
        session['Sec_Tipo2'] = ""
        session['SecA_fecha2'] = ""
        session['SecA_nombre3'] = ""
        session['SecA_Tipo3'] = ""
        session['SecA_fecha3'] = ""
        return redirect(url_for("sectionHIPAA"))  # only when form submitted
    return render_template('SectionA1.html', form=form)


@app.route('/sectionHIPAA',methods=['GET', 'POST'])
def sectionHIPAA():
    form = SectionHIPAAForm()
    if form.validate_on_submit():
        session['3_Name'] = form.childLast.data + " " + form.childFirst.data + " " + form.childMiddle.data
        session['3_DOB'] = session['APPLICANT_DOB']
        session['3_Describe'] = form.describeInfo.data
        session['3_agency'] = form.agency.data
        session['3_Date1'] = form.requestDate.data
        session['3_Date2'] = form.authorizationDate.data
        session['3_padre'] =  session['secB_Name']
        return redirect(url_for("release"))  # only when form submitted

    return render_template('HIPAA.html', form=form)

@app.route('/release',methods=['GET', 'POST'])
def release():
    form = SectionReleaseForm()
    if form.validate_on_submit():
        print("In release")
        session['4_Name1'] = session['secA_AppName']
        session['4_DOB'] = session['APPLICANT_DOB']
        session['4_Date1'] = session['3_Date1']
        session['MedicalPro'] = form.office.data
        print("before office var setting")
        if form.office.data == 'Chandler':
            session['DDD_Address1'] = '125 E Elliot Rd'
            session['4_Zip1'] = '85225'
            session['4_State1'] = 'AZ'
            session['4_City1'] = 'Chandler'
            session['4_Fax1'] = '(602) 542- 6870'
            session['4_Phone1'] = '(480) 831-1009'
        elif form.office.data == 'Flagstaff':
            session['DDD_Address1'] = '1701 N 4th St'
            session['4_Zip1'] = '86004'
            session['4_State1'] = 'AZ'
            session['4_City1'] = 'Flagstaff'
            session['4_Fax1'] = '(602) 542- 6870'
            session['4_Phone1'] = '(928) 637-0960'
        elif form.office.data == 'Tucson':
            session['DDD_Address1'] = '1455 S Alvernon Way'
            session['4_Zip1'] = '85711'
            session['4_State1'] = 'AZ'
            session['4_City1'] = 'Tucson'
            session['4_Fax1'] = '(602) 542- 6870'
            session['4_Phone1'] = '(520) 638-2600'
        elif form.office.data == 'Phoenix (Oeste)':
            session['DDD_Address1'] = '4622 W Indian School Ste #D-12'
            session['4_Zip1'] = '85031'
            session['4_State1'] = 'AZ'
            session['4_City1'] ='Phoenix'
            session['4_Fax1'] = '(602) 542- 6870'
            session['4_Phone1'] ='(602) 771-8888'
        else:
            session['DDD_Address1'] = '11420 N 19th Ave'
            session['4_Zip1'] = '85029'
            session['4_State1'] = 'AZ'
            session['4_City1'] = 'Phoenix'
            session['4_Fax1'] = '(602) 542- 6870'
            session['4_Phone1'] = '(602) 485-0236'
        print("office info set")
        session['InfoTipo1'] = form.InfoTipo1.data
        session['InfoTipo2'] = form.InfoTipo2.data
        session['InfoTipo3'] = form.InfoTipo3.data
        session['InfoTipo4'] = form.InfoTipo4.data
        session['InfoTipo5'] = form.InfoTipo5.data
        session['InfoTipo6'] = form.InfoTipo6.data
        session['InfoTipo7'] = form.InfoTipo7.data
        session['InfoTipo8'] = form.InfoTipo8.data
        session['InfoTipo9'] = form.InfoTipo9.data
        session['InfoTipo10'] = form.InfoTipo10.data
        session['InfoTipo11'] = form.InfoTipo11.data
        print("Infotipos complete")
        session['4_Specify1'] = form.other.data
        session['4_padre'] = session['secB_Name']
        session['4_Date2'] = session['3_Date1']
        print("I am at the end of release")
        return redirect(url_for("goodbye"))  # only when form submitted

    return render_template('Release.html', form=form)



@app.route('/goodbye', methods=['GET', 'POST'])
def goodbye():
    #some of the spanish variables are actually in english jajajajajajajajajajaj
    #I regret not looking at these variables sooner


        all_pdf_fields = ['secA_AppName','APPLICANT_DOB','APPLICANT_Sex','secA_AHCCCS','secA_Language','secA_HomeAddress','secA_City1', 'secA_State1','secA_Zip1','SecA_Phone','secA_Ethnicity','secA_Tribe','secA_MailingAdd', 'secA_City2','secA_State2','secA_Zip2','secA_ContactPrefer', 'secA_Contact','secA_Vote',
                      'SecA_nombre1', 'SecA_Tipo1', 'SecA_fecha1', 'SecA_nombre2','Sec_Tipo2','SecA_fecha2','SecA_nombre3','SecA_Tipo3','SecA_fecha3',
                      'secB_Name', 'secB_Relationship1', 'secB_Phone1', 'secB_Email1', 'secB_City1','secB_State1','secB_Zip1','secB_Relationship2','secB_Address1','secB_BestWay','secB_Phone2','secB_Alt','secB_LGName','secB_Address2', 'secB_City2', 'secB_Zip2', 'secB_State2',
                      'secC_tipo1','secC_plan1','secC_Titular1','secC_num1', 'secC_vigencia1','secC_naci1','secC_tipo2','secC_plan2','secC_Titular2','secC_num2','secC_vigencia2','secC_naci2',
                      'secD_estado1', 'secD_tipo1','secD_fechas1', 'secD_estado2','secD_tipo2', 'secD_fechas2','SIG_Name','SIG_Relationship','SIG_Date',
                      '3_DOB', '3_Name', '3_Describe', '3_Date1','3_agency','3_padre','3_Date2',
                      '4_Name1','4_DOB', '4_Date1','MedicalPro', 'DDD_Address1','4_Zip1', '4_State1', '4_City1','4_Fax1', '4_Phone1', 'InfoTipo1', 'InfoTipo2','InfoTipo3', 'InfoTipo4','InfoTipo5','InfoTipo6','InfoTipo7', 'InfoTipo8','InfoTipo9','InfoTipo10', '4_Specify1', 'InfoTipo11','4_padre','4_Date2']  # not the real field names, especially in the Spanish version!

        data_for_pdf = {}

        for key in all_pdf_fields:
            if key not in session:
                print(key + " is not here :(")
                #could help me debug if I have any spelling issues
            else:
                data_for_pdf[key] = session[key]

        complete_pdf = fill_one_pdf("DDD-2069A-S", data_for_pdf)
        return send_file(complete_pdf, as_attachment=True)


@app.route('/test', methods=['GET', 'POST'])
def test():
    # for the other classes, I can just so SectionB.variable.data to grab the info
    form = SectionAForm()
    if form.validate_on_submit():
        print("HERE")
        data_for_pdf = dict(
            secA_Contact = form.childEmail.data,
            secA_ContactPrefer = form.childEmail.data
        )
        complete_pdf = fill_one_pdf("DDD-2069A-S", data_for_pdf)
        return send_file(complete_pdf, as_attachment=True)
    else:
        return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
