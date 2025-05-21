from services import *

read_pam_settings(label_id=90243)
read_pam_settings(label_id=90245)
read_pam_settings(label_id=90248)

write_pam_settings(label_id=90243,
                    new_act_mg = 180,
                    new_deact_mg = 70,
                    new_deact_time_s = 120,
                    new_adv_byte = 0x15,       # encodes 5 → 546.25 ms (lower four bits = 5, multiplier=0)
                    new_conn_ms = 50.0)
write_pam_settings(label_id=90245,
                    new_act_mg = 180,
                    new_deact_mg = 70,
                    new_deact_time_s = 120,
                    new_adv_byte = 0x15,       # encodes 5 → 546.25 ms (lower four bits = 5, multiplier=0)
                    new_conn_ms = 50.0)
write_pam_settings(label_id=90248,
                    new_act_mg = 180,
                    new_deact_mg = 70,
                    new_deact_time_s = 120,
                    new_adv_byte = 0x15,       # encodes 5 → 546.25 ms (lower four bits = 5, multiplier=0)
                    new_conn_ms = 62.0)

read_pam_settings(label_id=90243)
read_pam_settings(label_id=90245)
read_pam_settings(label_id=90248)