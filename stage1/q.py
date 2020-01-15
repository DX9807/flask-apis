
def getcookie():
    try:
        table = dynamodb.Table('nb_users')
        user_id=request.cookies.get('user_id')
        response = table.query(IndexName = 'user_id', KeyConditionExpression=Key('user_id').eq(user_id))
        user = response.get('Items')
        if user!=[]:
            return res({'error': False, 'msg': 'you are logged in as.'+user[0]['user_name']})
        else:
            return res({'error': False, 'msg': 'Please login.'})
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})


def set_session(user):
    try:
        session['user_id']=user[0].get('user_id')
        session['email']=user[0].get('email')
        session['user_name']=user[0].get('user_name')
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})

######################Quiz Api#################################################
@app.route('/add_ques', methods =['POST'])
def add_ques():
    branch= CLIENT
    timestamp = time.time()
    if request.method == 'POST':
        question = request.form.get('question')
        option_1 = request.form.get('option_1')
        option_2 = request.form.get('option_2')
        option_3 = request.form.get('option_3')
        option_4 = request.form.get('option_4')
        answer   = request.form.get('answer')
        category = request.form.get('category')
        quiz_no = request.form.get('quiz_no')

    try:
        user=client.put_item(
                        TableName = 'questions',
                        Item = {
                                "branch":{'S':branch},
                                "ques_id":{'S':str(int(uuid4()))},
                                "created_on":{'N':str(int(timestamp))},
                                "question":{'S':question},
                                "options":{'L':[{'S':option_1},{'S':option_2},{'S':option_2},{'S':option_2}]},
                                "answer" :{'S':answer},
                                "category":{'S':category},
                                "quiz_no":{'N':str(quiz_no)},

                            })
        return res({'error': False, 'msg': 'Question Added.'})
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})



@app.route('/edit_ques/<int:created_on>', methods=['PUT'])
def edit_ques(created_on):
    branch = CLIENT
    created_on = created_on
    ques_id =str(ques_id)
    timestamp = time.time()
    question = request.form.get('question')
    option_1 = request.form.get('option_1')
    option_2 = request.form.get('option_2')
    option_3 = request.form.get('option_3')
    option_4 = request.form.get('option_4')
    answer   = request.form.get('answer')
    category = request.form.get('category')
    table = dynamodb.Table('questions')
    try:
        table.update_item(
                            Key = {
                                   'branch':branch,
                                   'created_on':created_on
                                   },
                            UpdateExpression="set updated_on=:a,question=:b,options=:c,answer=:h,category=:g",
                            ExpressionAttributeValues = {
                                    ":a":str(int(timestamp)),
                                    ":b":question,
                                    ":c":{'L':[{'S':option_1},{'S':option_2},{'S':option_3},{'S':option_4}]},
                                    ":h":answer,
                                    ":g":category,
                                },
                                ReturnValues="UPDATED_NEW"
                                )
        return res({'error': False, 'msg': 'Question updated.'})
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})



@app.route('/get_ques', methods=['GET'])
def get_ques():
    branch = CLIENT
    try:
        table = dynamodb.Table('questions')
        response=table.query(
                    KeyConditionExpression = Key('branch').eq(branch),
                    Limit=10
        )
        print(response)
        return res({'error': False, 'msg': 'Question updated.'})
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})


@app.route('/del_ques/<int:created_on>', methods=['DELETE'])
def del_ques(created_on):
    branch = CLIENT
    created_on= created_on
    try:
        table = dynamodb.Table('questions')
        item = table.delete_item(
                            Key={
                                'branch': branch,
                                'created_on': created_on
                            },
                            )
        print(item)
        return res({'error': False, 'msg': 'Question Deleted.'})
    except Exception as e:
        return res({'error': True, 'msg': 'Operation failed', 'errmsg': str(e)})


