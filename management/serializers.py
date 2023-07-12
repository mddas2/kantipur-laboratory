from .models import MicroObservationTable,ClientCategory,SuperVisorSampleForm, SampleForm, Commodity, CommodityCategory, MicroParameter , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate
from rest_framework import serializers
from account.models import CustomUser
from . import roles
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from . raw_data import generateRawData,UpdategenerateRawData
from .status_naming import over_all_status


class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','id'] 

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'        

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__' 
        

class CommodityReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CommodityRead_management"
        model = Commodity
        fields = ['id','name','name_nepali']

class TestResultSerializer(serializers.ModelSerializer):
    commodity = CommodityReadSerializer(many=False,read_only = True)
    class Meta:
        model = TestResult
        fields = '__all__'


class CommoditySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = '__all__'
        

class MicroObservationTableSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
            print(data['sample_form'])
        return super().to_internal_value(data)
    
    class Meta:
        model = MicroObservationTable
        fields = '__all__' 

class MicroParameterSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
            print(data['sample_form'])
        return super().to_internal_value(data)
    micro_observation_table = MicroObservationTableSerializer(many = True,read_only = True)
    class Meta:
        model = MicroParameter 
        fields = '__all__' 

# class CommoditySerializer(serializers.ModelSerializer):
#     class Meta:
#         ref_name = "Commodity_sample_form"
#         model = Commodity
#         fields = '__all__


class SampleFormReadSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    parameters = TestResultSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True,many=True)

    owner_user = serializers.SerializerMethodField()
    approved_by = ApprovedBySerializer(read_only = True,many=False)
    verified_by = ApprovedBySerializer(read_only = True,many=False)
    supervisor_user = ApprovedBySerializer(read_only = True)

    commodity = CommoditySerializer(read_only = True,many=False)
    
    class Meta:
        approved_by = ApprovedBySerializer(read_only = True)
        supervisor_user = ApprovedBySerializer(read_only = True)
        verified_by = ApprovedBySerializer(read_only = True)
        model = SampleForm
        fields = '__all__'

    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        parameters_data = representation.get('parameters', [])

        assigned = 0
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = smple_frm_exist.exists()
            parameter_data['exist'] = exists

            smple_frm_exist_for_supervisor = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
            exists_supervisor_parameter = smple_frm_exist_for_supervisor.exists()
            parameter_data['exists_supervisor_parameter'] = exists_supervisor_parameter

            if exists_supervisor_parameter:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status_supervisor'] = "assigned"
                    parameter_data['supervisor_user'] = smple_frm_exist_for_supervisor.first().supervisor_user.username
                except:
                    pass 

            if exists:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status'] = "assigned"
                    parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
                except:
                    pass           


            if exists == True:
                assigned+=1

        representation['total_assign'] = assigned
        representation['parameters'] = parameters_data
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"


        return representation



class SampleFormWriteSerializer(serializers.ModelSerializer):
    def validate(self, data):
        action = self.context['view'].action
        if action == "create" or action=="update":
            parameters = data.get('parameters')
            
            #id = data.get('id')
            commodity = data.get('commodity')
            commodity_parameters = TestResult.objects.filter(commodity=commodity)
            commodity_price = Commodity.objects.get(id = commodity.id).price
            if len(parameters) == 0:        
                data['parameters'] = commodity_parameters
                data['price'] = commodity_price
            else:
                # commodity_parameter_len =  commodity_parameters.count()
                # parameter_len = len(parameters)
                # if commodity_parameter_len == parameter_len:
                #     data['price'] = commodity_price
                # else:
                price = 0
                for paramet in parameters:
                    price = paramet.price + price
                print(price)
                data['price'] = price
                
            return data
        elif action == "partial_update" or action == "update":
            supervisor_user = data.get('supervisor_user')
            form_available = data.get('form_available')
       
            if supervisor_user is not None and form_available == "supervisor":
                request = self.context.get('request')
                data['approved_by'] = request.user
            return data
        else:
            return data
        
    class Meta:
        model = SampleForm
        fields = '__all__'

class SampleFormReadAnalystSerializer(serializers.ModelSerializer):
    commodity = CommodityReadSerializer(read_only=True,many=False)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = ApprovedBySerializer(read_only = True)

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    def validate(self, data):
        action = self.context['view'].action
        if action == "create":
            parameters = data.get('parameters')
            
            #id = data.get('id')
            if len(parameters) == 0:
                commodity = data.get('commodity')   
                parameters = TestResult.objects.filter(commodity=commodity)
                data['parameters'] = parameters
            return data
        else:
            return data
        
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    class Meta:
        
        model = SampleForm
        fields = '__all__'


class CommodityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'
   
class CommodityCategorySerializer(serializers.ModelSerializer):
    def validate_name(self,value):#field level validation
        if value == "test":
            raise serializers.ValidationError('name test should not be there error')
        return value
    
    def validate(self, data):
        name = data.get('name')
        #id = data.get('id')
        if name == "test":
            raise serializers.ValidationError('name test should not be there error')
        return data
    
    commodity = CommoditySerializer(many=True,read_only=True)
    class Meta:
        model = CommodityCategory
        fields = '__all__'
        
class SuperVisorSampleFormWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperVisorSampleForm
        fields = '__all__'
    
    def validate(self, attrs):
        sample_form = attrs.get('sample_form')
        print(sample_form," not  printing this...")
        supervisor_user = attrs.get('supervisor_user')
        parameters = attrs.get('parameters')

        action = self.context['view'].action
        
        print(parameters, " supervisor paaraameters")
        if len(attrs) == 3 and action == 'partial_update' and 'is_supervisor_sent' and 'status' and 'remarks' in attrs:
            if attrs.get('is_supervisor_sent') == True:
                id=self.context['view'].kwargs.get('pk')
                remarks  = attrs.get('remarks')
                UpdategenerateRawData(id,remarks) #  if sent to supervisor then generate logs
                return attrs
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')
        if action == "create" and len(parameters)>1:
            for param in parameters:
                
                if SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists():
                    raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and parameter already exists(create)')
        elif action == "create" and len(parameters) == 1:
            for param in parameters:
                
                if SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists():
                    sample_form_has_parameters_check = SampleFormHasParameter.objects.filter(sample_form = sample_form, parameter = param).exists()
                    if sample_form_has_parameters_check == False:
                        print("False mk")
                        attrs['re_assign'] = True 
                    else:                         
                        print("True mk")
                        raise serializers.ValidationError('Umesh sir You cant do this ...ammm, reasign karna band karo')
            
        
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
        
            sample_form_has_parameter_obj = SuperVisorSampleForm.objects.get(id=instance_id)  

            if SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                pass

            else:
                raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and analyst already exists(update)')
            
            for param in parameters:
                if sample_form_has_parameter_obj.parameters.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    pass
                elif SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and parameter already exists(update)')
                
        return attrs
    
    def create(self, validated_data):
        print(" create tes md f sadsd s")
       
        sample_form = validated_data['sample_form']
        supervisor_user = validated_data['supervisor_user']
        parameters = validated_data['parameters']
        test_type = validated_data['test_type']
        
        re_assign = validated_data.get('re_assign', False)    
        
        print(re_assign)
        
        if re_assign == True:
            
            obj = SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=parameters[0]).first()
            print(obj)
            print(obj.parameters.all())
            
            if len(obj.parameters.all())>1:
                
                obj.parameters.remove(*parameters) #revoke parameter from existence obj
                obj.is_supervisor_sent = False
                # AlterRawDataStatus(obj)  # supervisor doesnot need alter status
                obj.save()


                
                # flushsupervisorprameterCalculate(obj,parameters) # supervisor doesnot need flush analyst data
            

                instance = SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user)
                print(instance, " sdasd")
                if instance.exists():
                    print(2)
                    instance = instance.first()
                    #AlterRawDataStatus(instance)
                    instance.parameters.add(*parameters) #if particular supervisor already exist then add parameter to that analysts re-asign
                    instance.is_supervisor_sent = False
                  
                    return instance
                else:
                    print(supervisor_user,obj.sample_form_id,parameters)
                    print(3)
                    samp = SuperVisorSampleForm.objects.create(supervisor_user=supervisor_user,status="processing",sample_form_id=obj.sample_form_id,test_type = test_type)
                    samp.parameters.set(parameters)
                    samp.save()
                    
                    return obj
            else:
                if obj.supervisor_user == supervisor_user:
                    print(4)
                    return obj
                else:
                    # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
                    print(5)
                    instance = SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user)
                    print(instance," sadmd")
                    if instance.exists():
                        print("exists")
                        instance = instance.first()
                        #AlterRawDataStatus(instance.first())
                        instance.parameters.add(*parameters) #if particular analysts already exist then add parameter to that analysts re-asign
                        instance.supervisor_user = supervisor_user
                        instance.save()
                        obj.delete()
                        return instance
                    elif obj.parameters.all().first() == parameters[0]:
                        print(6)
                        print(obj.parameters.all(),'::',parameters)
                        obj.supervisor_user = supervisor_user
                        obj.parameters.add(*parameters)
                        obj.save()
                        return obj
                    else:
                        raise serializers.ValidationError('undefined assign supervisor rule')
                    
                    return obj
            # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
        print(sample_form," muk samaple ")
        eventOnSampleform(sample_form,parameters)
        print(6)
        if SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user).exists():
            print("testing ok append parameter")
            instance = SuperVisorSampleForm.objects.get(sample_form=sample_form, supervisor_user=supervisor_user)
            # Append the new parameters to the existing instance
            instance.parameters.add(*parameters)
            return instance
        
        return super().create(validated_data)


    
   
class SuperVisorSampleFormReadSerializer(serializers.ModelSerializer):  
    sample_form = SampleFormReadAnalystSerializer(read_only=True)
    commodity = CommodityWriteSerializer(read_only=True,many=True)
    parameters = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = SuperVisorSampleForm
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = instance.sample_form.id
        # print(sample_form_id,"sasdadada sdd ds")
        # sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        parameters_data = representation.get('parameters', [])

        assigned = 0
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = smple_frm_exist.exists()

            if exists:
                analyst_obj = smple_frm_exist.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = smple_frm_exist.first().status
                created_date = smple_frm_exist.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['sample_form_has_parameter'] = smple_frm_exist.first().id
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = over_all_status[formula_obj_result.first().status]
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    parameter_data['status'] = over_all_status['processing']
                    parameter_data['result'] = '-'

            parameter_data['exist'] = exists

            smple_frm_exist_for_supervisor = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
            exists_supervisor_parameter = smple_frm_exist_for_supervisor.exists()
            parameter_data['exists_supervisor_parameter'] = exists_supervisor_parameter

            if exists_supervisor_parameter:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status_supervisor'] = "assigned"
                    parameter_data['supervisor_user'] = smple_frm_exist_for_supervisor.first().supervisor_user.username
                except:
                    pass 

            # if exists:
            #     # print(smple_frm_exist.first().analyst_user.username)
            #     try:
            #         parameter_data['status'] = smple_frm_exist.first().status
            #         if smple_frm_exist.first().status == "not_verified":
            #             parameter_data['status'] = over_all_status['completed']
            #         parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
            #     except:
            #         pass           


            if exists == True:
                assigned+=1

        representation['total_assign'] = assigned
        representation['parameters'] = parameters_data
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed":
                representation['status'] = over_all_status[status]
            else:
                representation['status'] = over_all_status['processing']
                
        if request.user.role == roles.SUPERVISOR:
            representation['status'] = over_all_status[status]


        return representation
        

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    sample_form = SampleFormReadAnalystSerializer(read_only=True)
    # commodity = CommodityWriteSerializer(read_only=True,many=True)
    parameter = TestResultSerializer(many=True,read_only=True)
    assigned_by = serializers.SerializerMethodField()
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

    def get_assigned_by(self, obj):
        supervisor_table_obj = obj.super_visor_sample_form
        try:
            user = CustomUser.objects.get(id=supervisor_table_obj.supervisor_user.id)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def get_parameter(self, obj):
        parameter_data = TestResultSerializer(obj.parameter, many=True).data
  
        count_status = 0
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            if formula_calculate:
                parameter['result'] = formula_calculate.result               
                count_status = count_status + 1   
                parameter['input_fields_value'] = formula_calculate.input_fields_value
                parameter['status'] = formula_calculate.status
                parameter['remarks'] = formula_calculate.remarks
                parameter['is_locked'] = formula_calculate.is_locked
            else:
                parameter['result'] = ""      
         
        analyst_status = "processing"
        completed_done = 0
        recheck = False
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id)
            if formula_calculate.exists():
                if formula_calculate.first().result != None:
                    if formula_calculate.first().status == "recheck":
                        recheck = True                
                    analyst_status = "completed"   
                    completed_done = completed_done + 1
                else:
                    analyst_status = "tested"
                    break
            else:                
                analyst_status = "processing" 
                break     
                
        total_len = len(parameter_data)
        print(completed_done,"md",total_len)
        if completed_done == 0:
            completed_done = str(total_len)
        elif completed_done == total_len:
            completed_done = ''
            print(analyst_status)
        else:
            try:
                completed_done = str(completed_done) + "/" +str(total_len)                
            except:
                completed_done = str(total_len)+"/"+str(completed_done)
                
        

        if count_status == 0:
            analyst_status = "pending"      
        elif recheck == True:
            completed_done = ''
            analyst_status = "recheck" 
       
            
        return parameter_data,analyst_status,completed_done
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        parameter,analyst_status,total_completed = self.get_parameter(instance)
        representation['parameter'] = parameter

        print(instance.sample_form)
        if analyst_status == "completed" and instance.is_supervisor_sent == True:
            representation['status'] = over_all_status[instance.status]
        else:
            representation['status'] = analyst_status
        representation['completed_done'] = total_completed
        representation['completed_done'] = total_completed
        # representation['assigned_by'] = self.assigned_by

        return representation

class SampleFormHasParameterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
            print(data['sample_form'])
        return super().to_internal_value(data)
    
    def validate(self, attrs):
        sample_form = attrs.get('sample_form')
        print(attrs.get('super_visor_sample_form')," not  printing this...")
        analyst_user = attrs.get('analyst_user')
        parameter = attrs.get('parameter')

        action = self.context['view'].action
    
        if len(attrs) == 3 and action == 'partial_update' and 'is_supervisor_sent' and 'status' and 'remarks' in attrs:
            if attrs.get('is_supervisor_sent') == True:
                id=self.context['view'].kwargs.get('pk')
                remarks  = attrs.get('remarks')
                generateRawData(id,remarks) #  if sent to supervisor then generate logs
                return attrs
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')
  
        if action == "create" and len(parameter)>1:
            for param in parameter:
                
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(create)')
        elif action == "create" and len(parameter) == 1:
            for param in parameter:
                print(sample_form,param," re-assign debug")
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    attrs['re_assign'] = True                          
            
          
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
           
            sample_form_has_parameter_obj = SampleFormHasParameter.objects.get(id=instance_id)  

            if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                pass

            else:
                raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst already exists(update)')
            
            for param in parameter:
                if sample_form_has_parameter_obj.parameter.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    pass
                elif SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(update)')
                   
        return attrs
    
    def create(self, validated_data):
        print(" create tes md f")
       
        sample_form = validated_data['sample_form']
        analyst_user = validated_data['analyst_user']
        parameter = validated_data['parameter']
        
        re_assign = validated_data.get('re_assign', False)    
        
        print(re_assign,sample_form," sampl s")
        if re_assign == True:
            
            obj = SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=parameter[0]).first()
            
            if len(obj.parameter.all())>1:
                print(1)
                obj.parameter.remove(*parameter) #revoke parameter from existence obj
                obj.is_supervisor_sent = False
                AlterRawDataStatus(obj)
                obj.save()

                
                flushFormulaCalculate(obj,parameter)
            

                instance = SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user)
                print(instance, " sdasd")
                if instance.exists():
                    print(2)
                    instance = instance.first()
                    AlterRawDataStatus(instance)
                    instance.parameter.add(*parameter) #if particular analysts already exist then add parameter to that analysts re-asign
                    instance.is_supervisor_sent = False
                  
                    return instance
                else:
                    print(analyst_user,obj.sample_form_id,obj.commodity_id,parameter)
                    print(3)
                    samp = SampleFormHasParameter.objects.create(analyst_user=analyst_user,status="processing",commodity_id = obj.commodity_id,sample_form_id=obj.sample_form_id,form_available=obj.form_available,super_visor_sample_form = obj.super_visor_sample_form)
                    samp.parameter.set(parameter)
                    samp.save()
                    
                    return obj
            else:
                if obj.analyst_user == analyst_user:
                    print(4)
                    return obj
                else:
                    # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
                    print(5)
                    instance = SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user)
                    print(instance," ins md")
                    if instance.exists():
                        print("exists")
                        instance = instance.first()
                        AlterRawDataStatus(instance)
                        instance.parameter.add(*parameter) #if particular analysts already exist then add parameter to that analysts re-asign
                        instance.is_supervisor_sent = False
                        instance.save()
                        
                        obj.delete()

                        return instance
                    
                    return obj
            # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
        print(6)
        if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists():
            print("testing ok append parameter")
            instance = SampleFormHasParameter.objects.get(sample_form=sample_form, analyst_user=analyst_user)
            # Append the new parameters to the existing instance
            instance.parameter.add(*parameter)
            return instance
        
        return super().create(validated_data)

def flushFormulaCalculate(obj,parameter):
    formula_calculate_obj = obj.formula_calculate.all().filter(parameter_id = parameter[0])
    formula_calculate_obj.delete()
    print(formula_calculate_obj)
    print("flushing formula calculate")

def flushsupervisorprameterCalculate(obj,parameter):
    # formula_calculate_obj = obj.formula_calculate.all().filter(parameter_id = parameter[0])
    # formula_calculate_obj.delete()
    # print(formula_calculate_obj)
    print("flushing formula calculate")


def AlterRawDataStatus(obj):
    raw_data_obj = obj.raw_datasheet.all().last()
    print(raw_data_obj," obj none")
    if raw_data_obj == None:
        print("this sample form has parameter haave not raw data sheet")
    else:
        raw_data_obj.status = "re-assign"
        raw_data_obj.save()
    print("alter raw data status")

def eventOnSampleform(sample_form_id,parameters):
    sample_form_obj = sample_form_id

    sample_obj_params = sample_form_obj.parameters.all().count()
    supervisor_params = 0
    supervisor_objss = SuperVisorSampleForm.objects.filter(sample_form = sample_form_obj.id)
    for supervisor_ob in supervisor_objss: # if all supervisor analyst_test is True then update in sample form is_analyst_test = True
        params = supervisor_ob.parameters.all().count()
        supervisor_params = supervisor_params + params
    supervisor_params = supervisor_params + len(parameters)
   
    if sample_obj_params != supervisor_params:
        statuss = "not_assigned"
        form_availables = "smu"
        SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = False,status=statuss,form_available = form_availables)
    else:
        statuss = "processing"
        form_availables = "supervisor"
        SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = False,status=statuss,form_available = form_availables)
