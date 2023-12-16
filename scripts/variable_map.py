
# Columns

identificacao_columns = {
    'id_centro': 'center_id',
    'data_consulta_revisada': 'revised_consultation_date',
    'data_1a_consulta_centro': 'first_consultation_date_center',
    'data_1a_consulta_especialidade': 'first_consultation_date_specialty',
    'data_nascimento': 'birth_date',
    'idade': 'age',
    'raca_cor': 'color_or_race',
    'genero': 'sex',
    'cidade_nascimento': 'birth_city',
    'regiao_nascimento': 'birth_region',
    'pais_nasc': 'birth_country',
    'regiao_residencia': 'residence_region',
    'cidade_residencia': 'residence_city',
    'idade_1a_consulta_centro': 'age_at_first_evaluation_at_center',
    'idade_1a_consulta_especialidade': 'age_at_first_evaluation_at_specialty',
    'tempo_acompanhamento_centro': 'length_of_follow_up_at_center',
    'tempo_acompanhamento_especialidade': 'length_of_follow_up_at_specialty',
}

diagnostico_columns = {
    'id_centro': 'center_id',
    'status_diagnostico': 'diagnostic_status',
    'doenca_cid10': 'disease_cid10',
    'doenca_orpha': 'disease_orpha',
    'doenca_omim': 'disease_omim',
    'fonte_pagadora': 'diagnostic_payer_source',
    'momento_diagnostico': 'diagnostic_moment',
    'data_diagnostico': 'diagnostic_date',
    'sintomas': 'symptoms',
    'recorrencia_familiar': 'family_recurrence',
    'consanguinidade_relatada': 'consanguinity',
    'tipo_diagnostico': 'diagnostic_type',
    'idade_materna': 'maternal_age_at_birth',
    'idade_paterna': 'paternal_age_at_birth',
    'idade_inicio_sintomas_dias': 'age_at_symptoms_onset_days',
    'idade_inicio_sintomas': 'age_at_symptoms_onset',
    'idade_diagnostico': 'age_at_diagnosis',
    'odisseia_diagnostica': 'diagnostic_odyssey'
}

tratamento_columns = {
    'id_centro': 'center_id',
    'alvo_tratamento': 'treatment_related_to_rare_disease',
    'acompanha_outra_especialidade': 'follows_other_specialty',
    'outra_especialidade_medica': 'other_specialty',
    'especialidade_medica': 'medical_specialty',
    'todas_especialidades': 'all_specialties',
}

tipo_tratamento_columns = {
    'id_centro': 'center_id',
    'data_inicio': 'treatment_start_date',
    'fonte_pagadora': 'treatment_payer_source',
    'tipo_tratamento': 'treatment_type',
    'descricao': 'description',
    'idade_inicio_tratamento': 'age_at_treatment_start'
}

seguimento_columns = {
    'id_centro': 'center_id',
    'quantidade_internacoes': 'number_of_hospitalizations',
    'data_internacao': 'hospitalization_date',
    'cid_internacao': 'cid10_hospitalization',
    'ocorrencia_internacao': 'previous_hospitalization',
    'data_obito': 'death_date',
    'idade_obito': 'age_at_death',
    'necropsia_realizada': 'autopsy_performed',
    'cid_obito': 'cid10_death',
    'ocorrencia_obito': 'death',
}

# Variables

raca_cor = {
    'Branca': 'White',
    'Preta': 'Black',
    'Amarela': 'Yellow',
    'Parda': 'Brown',
    'Indigena': 'Indigenous',
}

genero = {
    'Feminino': 'Female',
    'Masculino': 'Male',
    'Indefinido': 'Undetermined',
}

regiao_nascimento = {
    'Norte': 'North',
    'Nordeste': 'Northeast',
    'Sudeste': 'Southeast',
    'Sul': 'South',
    'Centro-Oeste': 'Midwest',
    'Exterior': 'Born in other countries',
}

regiao_residencia = {
    'Norte': 'North',
    'Nordeste': 'Northeast',
    'Sudeste': 'Southeast',
    'Sul': 'South',
    'Centro-Oeste': 'Midwest',
}

status_diagnostico = {
    'Diagnóstico confirmado': 'Confirmed diagnosis',
    'Diagnóstico suspeito': 'Suspected diagnosis',
    'Sem diagnóstico': 'Undiagnosed',
}

momento_diagnostico = {
    'Pós-natal': 'Postnatal',
    'Triagem neonatal': 'Newborn screening',
    'Pré-natal': 'Prenatal',
}

recorrencia_familiar = {
    1: 'Yes',
    0: 'No',
}

consanguinidade_relatada = {
    1: 'Yes',
    0: 'No',
}

tipo_diagnostico = {
    'Clinico': "Clinical",
    'Etiologico Molecular': "Molecular (Etiological)",
    'Etiologico Bioquimico': "Biochemical (Etiological)",
    'Etiologico Anatomopatologico': "Anatomopathological (Etiological)",
    'Etiologico': "Etiological",
    'Etiologico Citogenetico': "Cytogenetic (Etiological)",
    'Clinico Molecular': "Molecular (Clinical)"
}

alvo_tratamento = {
    'Relacionado à doença rara': 'Related to rare disease',
    'Não relacionado à doença rara': 'Not related to rare disease',
}

acompanha_outra_especialidade = {
    1: 'Yes',
    0: 'No',
}

tipo_tratamento = {
    'Dietético': 'Diet therapy',
    'Reabilitação': 'Rehabilitation',
    'Medicamentoso': 'Drug therapy',
    'Outro': 'Other',
}

ocorrencia_internacao = {
    1: 'Yes',
    0: 'No',
}

ocorrencia_obito = {
    1: 'Yes',
    0: 'No',
}

necropsia_realizada = {
    1: 'Yes',
    0: 'No',
}