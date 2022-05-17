from flask import Flask, render_template, session, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import (StringField , SubmitField,BooleanField ,
                     RadioField , SelectField , TextField , TextAreaField)

from wtforms.validators import DataRequired
from util import fill_one_pdf

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


class SectionA(FlaskForm):
    childName = StringField('Full Name: ', validators=[DataRequired()])
    childDOB = StringField("Date of Birth: ", validators=[DataRequired()])
    childAddress = StringField('Address:', validators=[DataRequired()])
    childCity = StringField('City:', validators=[DataRequired()])
    childState = StringField('State:', validators=[DataRequired()])
    childZip = StringField('ZIP Code:', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    ethnicity = RadioField('Ethnicity:',
                         choices=[('Asian', 'Asian'), ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander') , ('White', 'White'), ('Black or African American', 'Black or African American'), ('American Indian / Alaskan Native'), ('American Indian / Alaskan Native')])
    tribe = StringField('Tribe (if applicable)')
    childMailAddress = StringField('Address:', validators=[DataRequired()])
    childMailCity = StringField('City:', validators=[DataRequired()])
    childMailState = StringField('State:', validators=[DataRequired()])
    childMailZip = StringField('ZIP Code:', validators=[DataRequired()])
    conpref = RadioField('Contact Preference:',
                         choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    email = TextAreaField('')
    conchoice = TextAreaField('')
    vote = RadioField('Do you want to register to vote?:',
                         choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField('Submit')


class SectionA1(FlaskForm):
    profName = StringField('Professionals name', validators=[DataRequired()])
    profPhone = StringField('Professionals phone', validators=[DataRequired()])
    type = StringField('Professional type', validators=[DataRequired()])
    date = StringField('Evaluation date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SectionB(FlaskForm):
    parentName = StringField('Full Name: ', validators=[DataRequired()])
    relationship = StringField("Relationship: ", validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    email = TextAreaField('')
    parentAddress = StringField('Address:', validators=[DataRequired()])
    parentCity = StringField('City:', validators=[DataRequired()])
    parentState = StringField('State:', validators=[DataRequired()])
    parentZip = StringField('ZIP Code:', validators=[DataRequired()])
    conpref = RadioField('Contact Preference:',
                         choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    legalName = StringField('Full Name: ', validators=[DataRequired()])
    legalRelationship = StringField("Relationship: ", validators=[DataRequired()])
    legalPhone = StringField('Phone', validators=[DataRequired()])
    legalAddress = StringField('Address:', validators=[DataRequired()])
    legalCity = StringField('City:', validators=[DataRequired()])
    legalState = StringField('State:', validators=[DataRequired()])
    legalZip = StringField('ZIP Code:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SectionC(FlaskForm):
    coverage = StringField('Type of Coverage:', validators=[DataRequired()])
    healthPlan = StringField('Name of Health Plan:', validators=[DataRequired()])
    policyName = StringField('Policy Holder Name:', validators=[DataRequired()])
    IDNum = StringField('ID/Group Number:', validators=[DataRequired()])
    policyNum = StringField('Policy Number:', validators=[DataRequired()])
    date = StringField('Effective Date:', validators=[DataRequired()])
    dob = StringField("Policy Holder's Date of Birth:", validators=[DataRequired()])
    submit = SubmitField('Submit')

class SectionD(FlaskForm):
    program = StringField('Early Intervention Program or School Name and School District:', validators=[DataRequired()])
    type = StringField('Type of Support(IEP or 504 plan)', validators=[DataRequired()])
    date = StringField('Dates Attended:', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
    form = TestForm()
    if form.validate_on_submit():
        print("HERE")
        data_for_pdf = dict(
            SecA_Name=form.name.data,
            appDOB=form.dob.data
        )
        complete_pdf = fill_one_pdf("DDD-2069A", data_for_pdf)
        return send_file(complete_pdf, as_attachment=True)
    else:
        return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
