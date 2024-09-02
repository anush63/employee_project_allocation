import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_authenticator import Authenticate
from yaml.loader import SafeLoader
st.title("EMPLOYEE PROJECT ALLOCATION AND MANAGEMENT")

with open('config.yaml') as file:
    config=yaml.load(file,Loader=SafeLoader)

authenticator=Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status,username=authenticator.login('Login','main')

if authentication_status:
    authenticator.logout('Logout','main')
    st.write(f'Wellcome *{name}*')
    import streamlit as st
    import mysql.connector

    myconn = mysql.connector.connect(host="localhost", user="root", password="", database="project_allocation")
    # creating the cursor object
    mycursor = myconn.cursor()

    st.markdown("please give the input")

    # side bar
    st.sidebar.title("select the operation")
    st.sidebar.markdown("select the options accordingly")

    choice = st.sidebar.selectbox("select", ("EMPLOYEE", "PROJECT", "ALLOCATE"))
    select_status = st.sidebar.selectbox("select the number", options=['INSERT', 'DISPLAY', 'UPDATE', 'DELETE'])

    if choice == "EMPLOYEE":
        if select_status == "INSERT":

            st.title("INSERT OPERATION")
            eid = st.number_input("enter employee id:")
            ename = st.text_input("enter ur name:")
            email = st.text_input("enter ur email id")
            mobile = st.number_input("enter ur mobile number:")
            designation = st.text_input("designation")
            address = st.text_input("enter ur address:")
            exp_year = st.text_input("experience year:")
            BOD = st.text_input("enter ur date of birth:")
            add_id = st.number_input("enter ur adhar number:")
            passport = st.text_input("pass port:")
            options = ["java", "python", "web", "android", "IOS"]
            skills = st.selectbox("skills", options)
            pid = st.number_input("enter project id:")
            p_status = st.text_input("enter ur project status:")
            p_sub_date = st.text_input("enter project submission date:")


            def insert():

                sql = "insert into emp_reg(eid,ename,email,mobile,designation,address,exp_year,BOD,add_id,passport,skills,pid,p_status,p_sub_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # the row values are provided in the form of tuple
                val = (
                    eid, ename, email, mobile, designation, address, exp_year, BOD, add_id, passport, skills, pid,
                    p_status,
                    p_sub_date)

                try:
                    # inserting the values into the table
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("registration successful")
                    print(mycursor.rowcount, "record inserted")
                except Exception as e:
                    print("u con not process", e)


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('SUBMIT', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                # name =st.text_input('Name',on_change=set_state,args=[2])
                insert()

        elif select_status == "DISPLAY":

            def display():
                st.title("DISPLAY OPERATION")

                try:
                    mycursor.execute("select * from emp_reg")
                    # fetching the rows from the cursor object
                    result = mycursor.fetchall()
                    st.table(result)

                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)
                st.info("click a button to proceed:")


            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('Display', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                display()

        elif select_status == 'UPDATE':
            ename = st.text_input("Enter ename")
            eid = st.number_input("Enter eid")


            def update():
                try:
                    sql = "update emp_reg set ename=%s where eid =%s"
                    val = (ename, eid)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Updated Successfully!!!")


                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            st.info("click a button to proceed:")

            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('UPDATE', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                update()

        elif select_status == 'DELETE':
            def delete_record(table, condition, value):
                try:
                    sql = f"DELETE FROM {table} WHERE {condition}"
                    val = (value,)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Deleted Successfully!!!")
                except Exception as e:
                    print("Cannot process:", e)
                    myconn.rollback()


            if choice == 'EMPLOYEE':
                eid = st.number_input("Enter eid")

            if st.button('DELETE'):
                delete_record('emp_reg', 'eid = %s', eid)

    elif choice == "PROJECT":
        if select_status == "INSERT":
            pid = st.number_input("PID:")
            pname = st.text_input("PNAME:")
            pdesc = st.text_input("Description:")
            pduration = st.number_input("Duration:")
            pskills = st.text_input("Skills:")
            assign_to = st.number_input("Assign to:")


            def insert():
                import mysql.connector
                myconn = mysql.connector.connect(host="localhost", user="root", password="",
                                                 database="project_allocation")
                # creating the cursor object
                mycursor = myconn.cursor()

                sql = "insert into proj_reg(pid,pname,pdesc,pduration,pskills,assign_to) values(%s,%s,%s,%s,%s,%s)"
                # the row values are provided in the form of tuple
                val = (pid, pname, pdesc, pduration, pskills, assign_to)

                try:
                    # inserting the values into the table
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("registration successful")
                    print(mycursor.rowcount, "record inserted")
                except Exception as e:
                    print("u con not process", e)


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('SUBMIT', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                # name =st.text_input('Name',on_change=set_state,args=[2])
                insert()
        elif select_status == "DISPLAY":

            def display():
                st.title("DISPLAY OPERATION")

                try:
                    mycursor.execute("select * from emp_reg")
                    # fetching the rows from the cursor object
                    result = mycursor.fetchall()
                    st.table(result)

                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)
                st.info("click a button to proceed:")


            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('Display', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                display()

        elif select_status == 'UPDATE':
            pid = st.number_input("Enter pid")
            pname = st.text_input("PNAME:")


            def update():
                try:
                    sql = "update proj_reg set pname=%s where pid =%s"
                    val = (pname, pid)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Updated Successfully!!!")


                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            st.info("click a button to proceed:")

            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('UPDATE', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                update()

        elif select_status == 'DELETE':
            def delete(table, condition, value):
                try:
                    sql = f"DELETE FROM {table} WHERE {condition}"
                    val = (value,)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Deleted Successfully!!!")
                except Exception as e:
                    print("Cannot process:", e)
                    myconn.rollback()


            if choice == 'PROJECT':
                pid = st.number_input("Enter pid")

            if st.button('DELETE'):
                delete('proj_reg', 'pid = %s', pid)



    elif choice == "ALLOCATE":
        if select_status == 'INSERT':
            eid = st.number_input("employee id:")
            pid = st.number_input("project id:")
            ename = st.text_input("employee name")


            def add():
                sql = "insert into allocate(eid,pid,ename) values (%s,%s,%s)"
                # The row values are provided in the form of tuple
                val = (eid, pid, ename)
                try:
                    # inserting the values into the table
                    mycursor.execute(sql, val)
                    myconn.commit()  # commit the transaction
                    st.success("project allocated")

                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            st.info("click a button to proceed:")

            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('SUBMIT', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                add()

        elif select_status == 'DISPLAY':

            def display():

                try:
                    mycursor.execute("""
                            select proj_reg.pid,proj_reg.pname,allocate.eid,allocate.ename
                            from proj_reg
                            inner join allocate
                            on proj_reg.pid=allocate.pid;
                            """)
                    # fetching the rows from the cursor object
                    result = mycursor.fetchall()
                    st.table(result)

                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()


            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)


            st.info("click a button to proceed:")

            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('Display', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                display()

        elif select_status == 'UPDATE':
            pid = st.number_input("Enter pid")
            ename = st.text_input("Enter ename")
            eid = st.number_input("Enter eid")


            def update():
                try:
                    sql = "update allocate set ename=%s,pid=%s where eid =%s"
                    val = (ename, pid, eid)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Updated Successfully!!!")

                except Exception as e:
                    print("can not process", e)
                    myconn.rollback()

            def set_state(i):
                st.session_state.stage = i
                st.write("i value is:", i)

            st.info("click a button to proceed:")

            if 'stage' not in st.session_state:
                st.session_state.stage = 0

            if st.session_state.stage == 0:
                st.button('UPDATE', on_click=set_state, args=[1])

            if st.session_state.stage >= 1:
                update()

        elif select_status == 'DELETE':
            def delete_record(table, condition, value):
                try:
                    sql = f"DELETE FROM {table} WHERE {condition}"
                    val = (value,)
                    mycursor.execute(sql, val)
                    myconn.commit()
                    st.success("Record Deleted Successfully!!!")
                except Exception as e:
                    print("Cannot process:", e)
                    myconn.rollback()


            if choice == 'ALLOCATE':
                eid = st.number_input("Enter eid")

                if st.button('DELETE'):
                    delete_record('allocate', 'eid = %s', eid)

elif authentication_status==False:
    st.error('username/password is incorrect')

elif authentication_status==None:
    st.warning('please enter your username and password')