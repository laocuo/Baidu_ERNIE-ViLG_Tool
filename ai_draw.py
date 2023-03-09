import PySimpleGUI as sg
import ai_draw_request as ai_request
import ai_draw_query as ai_query
import json

sg.change_look_and_feel('DarkAmber')

layout = [
    [sg.Text('请输入应用密钥')],
    [sg.Text('API Key', size = (10, 1)), sg.Input('', key = '__AK__')],
    [sg.Text('Secret Key', size = (10, 1)), sg.Input('', key = '__SK__')],
    [sg.Text('请输入描述文本和风格')],
    [sg.Text('文本', size = (10, 1)), sg.Input(key = '__TEXT__')],
    [sg.Text('风格', size = (10, 1)), sg.Input('', key = '__STYLE__')],
    [sg.Text('任务', size = (10, 1)), sg.Input(key = '__TASK__')],
    [sg.Text('图片', size = (10, 1)), sg.Input(key = '__IMAGE__')],
    [sg.Button('请求'), sg.Button('查询'), sg.Button('退出')],
    [sg.Text('返回结果', size = (50, 8), key = '__RESULT__')]
]

window = sg.Window('这是一个百度AI绘图工具', layout, grab_anywhere = True)

while True:
    event, values = window.read()
    if event in (None, '退出'):
        break
    elif event == '请求':
        if values['__AK__'] == '' or values['__SK__'] == '':
            sg.PopupError('密钥不能为空,请去百度申请')
        else:
            if values['__TEXT__'] == '' or values['__STYLE__'] == '':
                sg.PopupError('文本或风格不能为空')
            else:
                result = ai_request.request(values['__AK__'], values['__SK__'], values['__TEXT__'], values['__STYLE__'])
                ret = json.loads(result)
                window['__RESULT__'].update(result)
                if 'data' in ret:
                    window['__TASK__'].update(ret['data']['taskId'])
        pass
    elif event == '查询':
        if values['__AK__'] == '' or values['__SK__'] == '':
            sg.PopupError('密钥不能为空,请去百度申请')
        else:
            if values['__TASK__'] == '':
                sg.PopupError('任务不能为空')
            else:
                result = ai_query.query(values['__AK__'], values['__SK__'], values['__TASK__'])
                ret = json.loads(result)
                window['__RESULT__'].update(result)
                if 'data' in ret and ret['data']['status'] == 1:
                    window['__IMAGE__'].update(ret['data']['img'])
                else:
                    sg.PopupOK('图片正在生成,请稍后再试')
        pass

window.close()