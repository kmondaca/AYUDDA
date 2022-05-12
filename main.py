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
    ParentName = StringField('Full Name: ', validators=[DataRequired()])
    ParentDOB = StringField("Date of Birth: ", validators=[DataRequired()])
    ParentAddress = StringField('Address:', validators=[DataRequired()])
    ParentCity = StringField('City:', validators=[DataRequired()])
    ParentState = StringField('State:', validators=[DataRequired()])
    ParentZip = StringField('ZIP Code:', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    ethnicity = RadioField('Ethnicity:',
                         choices=[('Asian', 'Asian'), ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander') , ('White', 'White'), ('Black or African American', 'Black or African American'), ('American Indian / Alaskan Native'), ('American Indian / Alaskan Native')])
    tribe = StringField('Tribe (if applicable)')
    ParentMailAddress = StringField('Address:', validators=[DataRequired()])
    ParentMailCity = StringField('City:', validators=[DataRequired()])
    ParentMailState = StringField('State:', validators=[DataRequired()])
    ParentMailZip = StringField('ZIP Code:', validators=[DataRequired()])
    conpref = RadioField('Contact Preference:',
                         choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    email = TextAreaField('')
    conchoice = TextAreaField('')
    vote = RadioField('Do you want to register to vote?:',
                         choices=[('Yes', 'Yes'), ('No', 'No')])
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
