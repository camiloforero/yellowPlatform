# encoding:utf-8
from __future__ import unicode_literals
from django_podio import api, tools
from django_documents import documentsApi
from django_mailTemplates import mailApi
import pdb

def run(appID, params, hook=None):
    ans = ""
    podioApi = api.PodioApi(appID)
    item = podioApi.get_item(params['item_id'], external_id=False)
    hook = hook.email_document_hook
    conditions = hook.conditions.all()
    all_conditions = True
    for condition in conditions:
        ans += unicode(condition)
        if condition.condition_type == "=":
            all_conditions = all_conditions and condition.value == item['values'][condition.field_id]['value']
            print item['values'][condition.field_id]['value']
    print ans
    if all_conditions:
        transformer_dict = {}
        related_transformer_dict = {}
        transformers = hook.transformers.all()
        attachments = []
        for transformer in transformers:
            if "#" in transformer.key:
                related_transformer_dict[transformer.key] = transformer.value
            else:
                transformer_dict[int(transformer.key)] = transformer.value
        data = tools.dictSwitch(item['values'], transformer_dict, related_transformer_dict, True)            
        print data
        flat_data = tools.flatten_dict(data)
        if hook.document:
            generator = documentsApi.ODTTemplate(hook.document.name + '.odt')#TODO: esto solo sirve con odts, toca formalizarlo 
            generated_document = generator.render(flat_data)
            file_name = hook.document.file_name + '.pdf'
            attachments.append({'filename':file_name, 'data': generated_document.read()})
            generated_document.seek(0)
            podioApi.appendFile(params['item_id'], file_name, generated_document)
        if hook.email_template:
            print hook.email_template.pk
            email = mailApi.MailApi(hook.email_template.name)
            from_email = tools.retrieve_email(hook.from_email, item)
            to_email = tools.retrieve_email(hook.to_email, item)
            if hook.cc_email:
                cc_email = tools.retrieve_email(hook.cc_email, item)
            else:
                cc_email = []
            print from_email
            print to_email
            status = email.send_mail(from_email, [to_email], flat_data, attachments=attachments)
        return status
    else:
        return ans
        
